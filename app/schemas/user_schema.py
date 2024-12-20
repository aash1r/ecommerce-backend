from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserResponse(UserBase):
    id: int
    created_At: datetime

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
