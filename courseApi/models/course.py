from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Integer, Date
from typing import List
from datetime import datetime


class Promotion(Base):
    __tablename__ = "promotion"
    id: Mapped[int] = mapped_column(primary_key=True)
    discount: Mapped[float] = mapped_column(Float(precision=1, asdecimal=True))
    courses: Mapped[List["Course"]] = relationship(
        back_populates="promotion", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{self.discount:.0%}"


class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(15))
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[str] = mapped_column(String(60))
    promotion_id: Mapped[int] = mapped_column(ForeignKey("promotion.id"))
    promotion: Mapped[Promotion] = relationship(back_populates="courses")
    duration: Mapped[int] = mapped_column(Integer)
    time_published: Mapped[Date] = mapped_column(
        Date, default=datetime.now(), nullable=False
    )
