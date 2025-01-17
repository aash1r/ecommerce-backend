from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database import get_db
from app.models import product_model
from app.models.product_model import Product
from app.models.rating_model import Rating
from app.schemas import product_schema
from app.schemas.user_schema import RoleEnum

router = APIRouter(tags=["Products"])


@router.post(
    "/admin/products/add-product",
    status_code=status.HTTP_201_CREATED,
    response_model=product_schema.ProductResponse,
)
def add_products(
    product: product_schema.ProductBase,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(RoleEnum.admin)),
):
    print(current_user.id)
    product_data = Product(**product.model_dump())
    db.add(product_data)
    db.commit()
    db.refresh(product_data)

    return product_data


@router.get(
    "/admin/products/get-products",
    status_code=status.HTTP_200_OK,
)
def get_all_products(
    db: Session = Depends(get_db),
):
    products = db.query(product_model.Product).all()
    return {"products": products}


@router.delete("/admin/products/delete-product/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(RoleEnum.admin)),
):
    name_product = (
        db.query(product_model.Product).filter(product_model.Product.id == id).first()
    )
    product = (
        db.query(product_model.Product).filter(product_model.Product.id == id).delete()
    )
    if product == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or already deleted",
        )
    db.commit()
    return {
        "message": f"product at {id} succesfully deleted",
        "name": f"{name_product.name}",
    }


@router.get("/api/products", response_model=List[product_schema.ProductResponse])
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    products = (
        db.query(product_model.Product)
        .filter(product_model.Product.category == category)
        .all()
    )

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products found in category {category}",
        )

    return products


@router.get(
    "/api/products/search",
    response_model=dict[str, List[product_schema.ProductResponse]],
)
def search_products(name: str, db: Session = Depends(get_db)):
    products = (
        db.query(product_model.Product)
        .filter(product_model.Product.name.ilike(f"%{name}%"))
        .all()
    )
    if not products:
        raise HTTPException(
            status_code=404, detail=f"Searched item {name} is not found!"
        )
    return {"products": products}


@router.get(
    "/api/products/deal-of-the-day", response_model=product_schema.DealOfTheDayResponse
)
def get_deal_of_the_day(db: Session = Depends(get_db)):
    avg_ratings = (
        db.query(
            Rating.product_id,
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.rating).label("rating_count"),
        )
        .group_by(Rating.product_id)
        .subquery()
    )

    highest_rated_product = (
        db.query(Product, avg_ratings.c.average_rating, avg_ratings.c.rating_count)
        .join(avg_ratings, Product.id == avg_ratings.c.product_id)
        .order_by(
            avg_ratings.c.average_rating.desc(), avg_ratings.c.rating_count.desc()
        )
        .first()
    )

    if not highest_rated_product:
        raise HTTPException(status_code=404, detail="No products found with ratings")

    product, average_rating, rating_count = highest_rated_product

    response = product_schema.DealOfTheDayResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        average_rating=average_rating,
        rating_count=rating_count,
    )

    return response
