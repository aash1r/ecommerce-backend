from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database import get_db
from app.models.cart_model import Cart
from app.models.product_model import Product
from app.schemas.cart_schema import CartItemCreate, CartItemResponse
from app.schemas.user_schema import RoleEnum

router = APIRouter(prefix="/api", tags=["Cart"])


@router.post("/cart/add", response_model=CartItemResponse)
def add_to_cart(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(RoleEnum.user)),
):
    print(current_user)
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    existing_cart_item = (
        db.query(Cart)
        .filter(
            Cart.user_id == current_user.id, Cart.product_id == cart_item.product_id
        )
        .first()
    )

    if existing_cart_item:
        existing_cart_item += cart_item.quantity
        existing_cart_item.total_price = existing_cart_item.quantity * product.price
        db.commit()
        db.refresh(existing_cart_item)
        return existing_cart_item

    new_cart_item = Cart(**cart_item.model_dump())
    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)
    return new_cart_item
