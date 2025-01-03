from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database import get_db
from app.models import rating_model
from app.models.product_model import Product
from app.schemas import rating_schema
from app.schemas.user_schema import RoleEnum

router = APIRouter(tags=["Rating"])


@router.post("/api/products/rate-product", response_model=rating_schema.RatingResponse)
def rate_products(
    rating: rating_schema.RatingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(RoleEnum.user)),
):
    product = db.query(Product).filter(Product.id == rating.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_rating = (
        db.query(rating_model.Rating)
        .filter(
            rating_model.Rating.product_id == rating.product_id,
            rating_model.Rating.user_id == current_user.id,
        )
        .first()
    )

    if existing_rating:
        existing_rating.rating = rating.rating
        db.commit()
    else:
        new_rating = rating_model.Rating(**rating.model_dump())
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)

    return existing_rating if existing_rating else new_rating
