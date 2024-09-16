import pytest
from httpx import AsyncClient
from fastapi import HTTPException
from courseApi.crud.user import create_user
from courseApi.schemas.user import UserInDB


@pytest.mark.anyio
async def test_user_register(async_client: AsyncClient):
    user_info = {"full_name": "amirhossein", "email": "amirhossein@gmail.com", "password": "1234"}
    result = await async_client.post("users/register", json=user_info)
    assert result.status_code == 201


@pytest.mark.anyio
async def test_user_register_email_duplicate(registered_user):
    user_info = {"full_name": "ali", "email": registered_user.get("email"), "password": "1234"}
    with pytest.raises(HTTPException):
        res = await create_user(UserInDB(**user_info))
        assert res.status_code == 400
