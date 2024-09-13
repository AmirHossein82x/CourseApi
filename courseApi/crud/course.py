from sqlalchemy import insert
from courseApi.models.course import Course
from courseApi.models import database


async def course_create(data):
    query = insert(Course).values(**data.model_dump())
    course_id = await database.execute(query)
    return course_id
