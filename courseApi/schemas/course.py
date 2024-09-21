from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


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


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    promotion_id: Optional[int] = None
    duration: Optional[int] = None
