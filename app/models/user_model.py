from sqlalchemy import TIMESTAMP, Column, Integer, String, text
from sqlalchemy.orm import relationship

from app.database import Base
from app.schemas.user_schema import RoleEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_At = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    role = Column(String, nullable=False, default=RoleEnum.user)
    ratings = relationship("Rating", back_populates="user")
    cart_items = relationship("Cart", back_populates="user")
