from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import utils
from app.database import get_db
from app.models.user_model import User
from app.schemas import user_schema

router = APIRouter(prefix="/api", tags=["Auth"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.UserResponse,
)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    hashed_password = utils.hash(user.password)
    user_data = user.model_dump()
    user_data["password"] = hashed_password
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
