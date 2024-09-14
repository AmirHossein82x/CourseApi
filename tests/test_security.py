import pytest
from courseApi.utils import security, hash
from fastapi import HTTPException
import jwt
from courseApi.config import config
from courseApi.utils.security import (
    create_access_token,
    authenticate_user,
    get_current_user,
)


SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await security.get_user_by_email(registered_user["email"])
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_password_hash():
    password = "1234"
    assert security.verify_password(password, hash.get_password_hash(password))


@pytest.mark.anyio
async def test_access_token():
    token = create_access_token({"sub": "amirhossein@gmail.com"})
    assert {"sub": "amirhossein@gmail.com"}.items() <= jwt.decode(
        token, key=SECRET_KEY, algorithms=[ALGORITHM]
    ).items()


@pytest.mark.anyio
async def test_authenticate_user(registered_user):
    user = await authenticate_user(
        registered_user["email"], password=registered_user["password"]
    )
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_authenticate_user_not_found():
    user = await authenticate_user("email", password="password")
    assert not user


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(registered_user):
    user = await authenticate_user(registered_user["email"], "123")
    assert not user


@pytest.mark.anyio
async def test_get_current_user_success(registered_user):
    token = create_access_token({"sub": registered_user["email"]})
    user = await get_current_user(token)
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_current_user_failed():
    token = create_access_token({"sub": "email"})
    with pytest.raises(HTTPException):
        await get_current_user(token)