from fastapi import APIRouter, Depends
from typing import Annotated
from courseApi.schemas.user import UserMe
from courseApi.utils.security import get_current_user
from courseApi.schemas.buy_course import CourseBoughtCreate
from courseApi.schemas.course import CourseShowToAll
from courseApi.crud.buy_course import (
    register_order as register_order_crud,
    get_course_ids,
    get_all_courses_for,
)
from typing import List
import logging


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/course-buy", tags=["course-buy"])


@router.post("/", status_code=201)
async def register_order(
    user: Annotated[UserMe, Depends(get_current_user)], item: CourseBoughtCreate
):
    logger.info(f"try to register order with user: {user.email} and course_id: {item.course_id}")
    await register_order_crud(user.id, item.model_dump())
    return {"detail": "order created"}


@router.get("/me", response_model=List[CourseShowToAll])
async def get_all_bought_course_for_user(
    user: Annotated[UserMe, Depends(get_current_user)]
):
    logger.info(f"get all courses for user id: {user.id}", extra={"email": user.email})
    course_ids = await get_course_ids(user)
    data = await get_all_courses_for(course_ids)
    return data
