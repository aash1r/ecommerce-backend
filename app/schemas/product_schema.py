from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    quantity: int
    price: int
    description: str
    images: str
    category: str


class ProductResponse(ProductBase):
    id: int
    description: str
    images: str
    category: str
