from pydantic import BaseModel


class RatingCreate(BaseModel):
    user_id: int
    product_id: int
    rating: float

    class Config:
        from_attributes = True


class RatingResponse(RatingCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
