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


class DealOfTheDayResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    average_rating: float
    rating_count: int

    class Config:
        from_attributes = True
