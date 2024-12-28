from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.database import get_db
from app.models.product_model import Product
from app.schemas import product_schema
from app.schemas.user_schema import RoleEnum

router = APIRouter(prefix="/api", tags=["Products"])


@router.post(
    "/admin/add-product",
    status_code=status.HTTP_201_CREATED,
    response_model=product_schema.ProductResponse,
)
def add_products(
    product: product_schema.ProductBase,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(RoleEnum.admin)),
):

    product_data = Product(**product.model_dump())
    db.add(product_data)
    db.commit()
    db.refresh(product_data)

    return product_data
