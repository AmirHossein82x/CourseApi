from courseApi.config import config
from courseApi.crud.user import create_user, update_user, password_reset
from courseApi.schemas.token import LoginToken, Token
from courseApi.schemas.user import UserInDB, User, UserMe, UserChangePassword
from courseApi.utils.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    verify_password,
)

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=201)
async def register(data: UserInDB):
    user_id = await create_user(data)
    return {"id": user_id, "email": data.email, "full_name": data.full_name}


@router.patch("/update")
async def update_user_info(
    user: Annotated[User, Depends(get_current_user)], item: User
):
    user_id = user.id
    await update_user(item, user.id)
    return {"id": user_id, **item.model_dump()}


@router.patch("/password-reset")
async def password_reset_user(
    user: Annotated[User, Depends(get_current_user)], item: UserChangePassword
):
    if verify_password(item.password, user.password):
        if item.new_password == item.new_password_retype:
            user_id = user.id
            await password_reset(item.new_password, user_id)
            return {"detail": "password changed successfully"}
        else:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "password and password retype are not same!",
            )
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "your password is not correct")


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
