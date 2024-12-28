from typing import Optional

from pydantic import BaseModel

from app.schemas.user_schema import RoleEnum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[RoleEnum] = None
