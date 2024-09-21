import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_course_success(
    async_client: AsyncClient, created_promotion, logged_in_token_for_admin
):
    data = {
        "title": "test",
        "description": "test test test",
        "price": 12000,
        "promotion_id": created_promotion,
        "duration": 20,
    }
    res = await async_client.post(
        "course/",
        json=data,
        headers={"Authorization": f"Bearer {logged_in_token_for_admin}"},
    )
    assert res.status_code == 201
    assert data.items() <= res.json().items()


@pytest.mark.anyio
async def test_create_course_fail(async_client: AsyncClient, logged_in_token_for_admin):
    data = {
        "title": "test",
        "description": "test test test",
        "price": 12000,
        "promotion_id": 0,
        "duration": 20,
    }
    res = await async_client.post(
        "course/",
        json=data,
        headers={"Authorization": f"Bearer {logged_in_token_for_admin}"},
    )
    assert res.status_code == 400


@pytest.mark.anyio
async def test_update_course(
    async_client: AsyncClient, logged_in_token_for_admin, created_course
):
    data = {"title": "ali reza", "duration": 20}
    res = await async_client.patch(
        f'course/{created_course.json()["slug"]}',
        json=data,
        headers={"Authorization": f"Bearer {logged_in_token_for_admin}"},
    )
    assert res.status_code == 200


@pytest.mark.anyio
async def test_delete_course(
    async_client: AsyncClient, logged_in_token_for_admin, created_course
):
    res = await async_client.delete(
        f'course/{created_course.json()["slug"]}',
        headers={"Authorization": f"Bearer {logged_in_token_for_admin}"},
    )
    assert res.json()["detail"] == "no content"
