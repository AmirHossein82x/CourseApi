from sqlalchemy import insert, select
from courseApi.models.course import CourseBought, Course
from courseApi.models import database
from fastapi import HTTPException, status


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
        return await database.execute(query)
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "you already bought this course")


async def get_course_ids(user):
    query = select(CourseBought).where(CourseBought.user_id == user.id)
    result = await database.fetch_all(query)
    print(result)
    return [item.course_id for item in result]


async def get_all_courses_for(course_ids):
    query = select(Course).where(Course.id.in_(course_ids))
    return await database.fetch_all(query)
