from courseApi.crud.user import get_user_by_email
from .hash import verify_password, oauth2_scheme
from datetime import datetime, timezone, timedelta
from courseApi.config import config
import jwt
from typing import Annotated
from courseApi.schemas.token import TokenData
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from courseApi.schemas.user import UserMe


async def authenticate_user(email: str, password: str):
    user = await get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user



async def isAdminUser(user: Annotated[UserMe, Depends(get_current_user)]):
    if user.is_admin:
        return user
    raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, "you are not allow to do this action")