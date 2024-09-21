from courseApi.models import database
from courseApi.models.user import User
from courseApi.schemas.user import UserInDB
from courseApi.utils.hash import get_password_hash
from fastapi import HTTPException, status
from sqlalchemy import select, insert, update
import logging


logger = logging.getLogger(__name__)


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
    except Exception as e:
        logger.error("email already exists", extra={"email": data.email})
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    logger.info("user is successfully registered", extra={"email": data.email})
    return user


async def update_user(item: User, pk: int):
    logger.info(f"update user id: {item.id}", extra={"email": item.email})
    query = update(User).where(User.id == pk).values(**item.model_dump())
    data = await database.execute(query)
    return data


async def password_reset(password, pk: int):
    logger.info(f"reset password for user {pk}")
    query = (
        update(User)
        .where(User.id == pk)
        .values({"password": get_password_hash(password)})
    )
    await database.execute(query)
