from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(db: Session = Depends(get_db)):
    new_user = User(
        id=1, username="aashir", email="aashirisani@gmial.com", hashed_password="123456"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
