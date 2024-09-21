from fastapi import APIRouter, Depends
from courseApi.schemas.course import CourseCreate, CourseShowToAll, CourseUpdate
from courseApi.schemas.user import UserMe
from courseApi.crud.course import (
    course_create,
    get_all_course,
    get_course_by_slug,
    update_course_crud,
    delete_course_by_slug,
)
from fastapi import HTTPException, status
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from courseApi.utils.security import isAdminUser
from typing import Annotated, List
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/course", tags=["course"])


@router.post("/", status_code=201)
async def create_course(
    item: CourseCreate, user: Annotated[UserMe, Depends(isAdminUser)]
):
    try:
        course_id = await course_create(item)
    except ForeignKeyViolationError:
        logger.error(f"error while attempting create course by {user.email} | no promotion with that id")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "no promotion with that id")
    except UniqueViolationError:
        logger.error(f"error while attempting create course by {user.email} | title already exists")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "title already exists")

    else:
        logger.info(f"course created successfully by {user.email}", extra={"email": user.email})
        return {"id": course_id, **item.model_dump()}


@router.get("/", response_model=List[CourseShowToAll])
async def show_all_courses():
    logger.info("get all courses")
    return await get_all_course()


@router.get("/{slug}")
async def show_course_by_slug(slug: str):

    course = await get_course_by_slug(slug)
    if course:
        logger.info(f"show detail of course {slug}")
        return CourseShowToAll(**course)
    logger.error(f"no course with that slug found slug: {slug}")
    raise HTTPException(404, "not found")


@router.patch("/{slug}")
async def update_course(slug: str, item: CourseUpdate, user: Annotated[UserMe, Depends(isAdminUser)]):
    try:
        course_id = await update_course_crud(slug, item.model_dump(exclude_none=True))
    except ForeignKeyViolationError:
        logger.error(f"no promotion with that id | id: {item.promotion_id}", extra={"email": user.email})
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "no promotion with that id")
    except UniqueViolationError:
        logger.error(f"title already exists | title: {item.title}", extra={"email": user.email})
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "title already exists")

    else:
        logger.info(f"course {slug} successfully updated by {user.email}", extra={"email": user.email})
        return {"id": course_id, **item.model_dump()}


@router.delete("/{slug}")
async def delete_course(slug: str, user: Annotated[UserMe, Depends(isAdminUser)]):
    logger.info(f"delete course {slug}")
    await delete_course_by_slug(slug)
    return {"detail": "no content"}



