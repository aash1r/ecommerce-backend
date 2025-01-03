from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import utils
from app.core import security
from app.database import get_db
from app.models.user_model import User

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(
    user_credits: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_credits.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not utils.verify(user_credits.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Passwords do not match"
        )

    access_token = security.create_access_token(data={"id": user.id, "role": user.role})

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "role": user.role,
        "user_id": user.id,
    }
