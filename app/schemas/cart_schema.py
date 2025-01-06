from typing import List

from pydantic import BaseModel


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 0


class CartItemResponse(CartItemCreate):
    id: int
    total_price: float

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_price: float
