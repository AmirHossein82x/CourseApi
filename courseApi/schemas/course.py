from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str
    description: str
    price: int
    promotion_id: int
    duration: int

