from courseApi.config import config
from courseApi.crud.user import create_user
from courseApi.schemas.token import LoginToken, Token
from courseApi.schemas.user import UserInDB, User, UserMe
from courseApi.utils.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated


router = APIRouter(prefix="/users")


@router.post("/register", status_code=201)
async def register(data: UserInDB):
    user_id = await create_user(data)
    return {"id": user_id, "email": data.email, "full_name": data.full_name}


@router.post("/jwt-create", status_code=201)
async def create_jwt(data: LoginToken):
    user = await authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserMe)
async def me(user: Annotated[User, Depends(get_current_user)]):
    return user
