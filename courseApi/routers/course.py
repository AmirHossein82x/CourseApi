from fastapi import APIRouter
from courseApi.schemas.course import CourseCreate
from courseApi.crud.course import course_create
from courseApi.models.course import Promotion
from sqlalchemy import select
from courseApi.models import database
from fastapi import HTTPException, status


router = APIRouter(prefix="/course", tags=["course"])


@router.post("/")
async def create_course(item:CourseCreate):
    promotion = select(Promotion).where(Promotion.id == item.promotion_id)
    if await database.fetch_one(promotion):
        course_id = await course_create(item)
        return {"id": course_id, **item.model_dump()}
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "no promotion with that id")