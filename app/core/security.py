from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import app
import app.schemas
import app.schemas.token_schema
from app.config import settings
from app.schemas.user_schema import RoleEnum

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINS = settings.access_token_expire_mins

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=("login"))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)

    to_encode.update({"expire": expire.timestamp()})

    jwt_encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encoded


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = str(payload.get("id"))
        role: str = payload.get("role")
        expire: float = payload.get("expire")

        if user_id is None or role is None:
            raise credentials_exception

        if datetime.utcnow().timestamp() > expire:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired!",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            role = RoleEnum(role)
        except ValueError:
            raise credentials_exception

        token_data = app.schemas.token_schema.TokenData(id=user_id, role=role)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)


def require_role(required_role: RoleEnum):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: {required_role} role required",
            )
        return current_user

    return role_checker
