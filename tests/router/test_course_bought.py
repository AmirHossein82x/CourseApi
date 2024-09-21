import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_register_order(
    async_client: AsyncClient, logged_in_token, created_course
):
    data = {
        "course_id": created_course.json()["id"],
        "price": created_course.json()["price"],
    }
    response = await async_client.post(
        "course-buy/", json=data, headers={"Authorization": f"Bearer {logged_in_token}"}
    )
    assert response.status_code == 201
