from sqlalchemy import insert, select, label
from courseApi.models.course import Course, Promotion
from courseApi.models import database
from slugify import slugify

async def course_create(data):
    model_dump = data.model_dump()
    query = insert(Course).values({**model_dump, "slug": slugify(model_dump.get("title"))})
    course_id = await database.execute(query)
    return course_id


async def get_all_course():
    final_price_label = label("final_price", Course.price * (1 - Promotion.discount))

    query = select(Course, final_price_label).join(
        Promotion, Course.promotion_id == Promotion.id
    )
    return await database.fetch_all(query)



async def get_course_by_slug(slug):
    final_price_label = label("final_price", Course.price * (1 - Promotion.discount))

    query = select(Course, final_price_label).where(Course.slug == slug).join(
        Promotion, Course.promotion_id == Promotion.id
    )
    return await database.fetch_one(query)