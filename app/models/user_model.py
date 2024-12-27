from sqlalchemy import TIMESTAMP, Column, Integer, String, text

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_At = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    role = Column(String, nullable=False)
