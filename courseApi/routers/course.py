from fastapi import APIRouter, Depends
from courseApi.schemas.course import CourseCreate
from courseApi.schemas.user import UserMe
from courseApi.crud.course import course_create
from fastapi import HTTPException, status
from asyncpg.exceptions import ForeignKeyViolationError
from courseApi.utils.security import isAdminUser
from typing import Annotated

router = APIRouter(prefix="/course", tags=["course"])


@router.post("/", status_code=201)
async def create_course(
    item: CourseCreate, user: Annotated[UserMe, Depends(isAdminUser)]
):
    try:
        course_id = await course_create(item)
    except ForeignKeyViolationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "no promotion with that id")
    else:
        return {"id": course_id, **item.model_dump()}
