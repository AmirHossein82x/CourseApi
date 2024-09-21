from typing import AsyncGenerator, Generator
import pytest
import os

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

os.environ["ENV_STATE"] = "test"
from courseApi.models import database
from courseApi.main import app
from courseApi.models.user import User
from sqlalchemy import select, insert, update
from courseApi.models.course import Promotion
from alembic.config import Config
from alembic import command


@pytest.fixture(scope="session", autouse=True)
def alembic_config():
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=client.base_url
    ) as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_detail = {
        "email": "test@gmail.com",
        "full_name": "testName",
        "password": "1234",
    }
    await async_client.post("users/register", json=user_detail)
    query = select(User).where(User.email == user_detail.get("email"))
    user = await database.fetch_one(query)
    user_detail["id"] = user.id
    return user_detail


@pytest.fixture()
async def registered_admin(async_client: AsyncClient) -> dict:
    user_detail = {
        "email": "test@gmail.com",
        "full_name": "testName",
        "password": "1234",
    }
    await async_client.post("users/register", json=user_detail)
    query = select(User).where(User.email == user_detail.get("email"))
    user = await database.fetch_one(query)
    updated = update(User).where(User.id == user.id).values({"is_admin": True})
    await database.execute(updated)

    user_detail["id"] = user.id

    return user_detail


@pytest.fixture()
async def logged_in_token(async_client: AsyncClient, registered_user):
    response = await async_client.post("users/jwt-create", json=registered_user)
    return response.json()["access_token"]


@pytest.fixture()
async def logged_in_token_for_admin(async_client: AsyncClient, registered_admin):
    response = await async_client.post("users/jwt-create", json=registered_admin)
    return response.json()["access_token"]


@pytest.fixture()
async def created_promotion():
    data = insert(Promotion).values({"discount": 0.5})
    res = await database.execute(data)
    return res


@pytest.fixture()
async def created_course(async_client: AsyncClient, logged_in_token_for_admin, created_promotion):
    data = {
        "title": "test",
        "description": "test test test",
        "price": 12000,
        "promotion_id": created_promotion,
        "duration": 20,
    }
    await async_client.post(
        "course/",
        json=data,
        headers={"Authorization": f"Bearer {logged_in_token_for_admin}"},
    )
    data["slug"] = "test"
    course = await async_client.get(f"course/{'test'}")
    return course
