from sqlalchemy import insert, select
from courseApi.models.course import CourseBought, Course
from courseApi.models import database
from fastapi import HTTPException, status
import logging


logger = logging.getLogger(__name__)


async def register_order(user_id: int, data):
    a = select(CourseBought).where(
        CourseBought.user_id == user_id, CourseBought.course_id == data.get("course_id")
    )
    course_bought = database.fetch_one(a)
    if not course_bought:
        query = insert(CourseBought).values(
            {
                "user_id": user_id,
                "course_id": data.get("course_id"),
                "payed": data.get("payed"),
            }
        )
        logger.info(f"user with id: {user_id} successfully bought course with id {data.get('course_id')}")
        return await database.execute(query)
    logger.error(f"user with id {user_id} already owned course id {data.get('course_id')}")
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "you already bought this course")


async def get_course_ids(user):
    query = select(CourseBought).where(CourseBought.user_id == user.id)
    result = await database.fetch_all(query)
    return [item.course_id for item in result]


async def get_all_courses_for(course_ids):
    query = select(Course).where(Course.id.in_(course_ids))
    return await database.fetch_all(query)
