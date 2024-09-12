from courseApi.models import database
from courseApi.models.user import User
from courseApi.schemas.user import UserInDB
from courseApi.utils.hash import get_password_hash
from fastapi import HTTPException, status
from sqlalchemy import select, insert


async def get_user_by_email(email: str):
    query = select(User).where(User.email == email)
    user = await database.fetch_one(query)
    if user:
        return user


async def create_user(data: UserInDB):
    query = insert(User).values(
        {
            "email": data.email,
            "full_name": data.full_name,
            "password": get_password_hash(data.password),
        }
    )
    try:
        user = await database.execute(query)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "email already exists!")
    return user
