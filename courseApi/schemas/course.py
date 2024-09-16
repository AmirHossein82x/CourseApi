from pydantic import BaseModel
from decimal import Decimal


class Promotion(BaseModel):
    id: int
    discount: Decimal

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    title: str
    description: str
    price: int
    promotion_id: int
    duration: int
    class Config:
        from_attributes = True



class CourseShowToAll(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    price: int
    promotion_id: int
    final_price: float
    duration: int

    class Config:
        from_attributes = True
