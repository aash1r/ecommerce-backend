from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import utils
from app.database import get_db
from app.models import user_model
from app.models.user_model import User
from app.schemas import user_schema

router = APIRouter(prefix="/api", tags=["Users"])


@router.post(
    "/users/register",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schema.UserResponse,
)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered!")

    if len(user.password) < 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be atleast 7 characters long!",
        )

    hashed_password = utils.hash(user.password)
    user_data = user.model_dump()
    user_data["password"] = hashed_password
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users/{id}")
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} not found",
        )
    return user


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    deleted_count = db.query(user_model.User).filter(user_model.User.id == id).delete()
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not found or already deleted!",
        )
    db.commit()
    return {"message": "user deleted!"}
