from pydantic import BaseModel
from datetime import date


class CourseCreate(BaseModel):
    title: str
    description: str
    price: int
    promotion_id: int
    duration: int

