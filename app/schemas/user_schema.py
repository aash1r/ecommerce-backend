from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str


class UserResponse(UserBase):
    id: int
    created_At: datetime
    role: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
