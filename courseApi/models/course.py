from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, Date, func, DECIMAL
from typing import List


class Promotion(Base):
    __tablename__ = "promotion"
    id: Mapped[int] = mapped_column(primary_key=True)
    discount: Mapped[float] = mapped_column(DECIMAL(2, 1))
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
    price: Mapped[int] = mapped_column(Integer)
    promotion_id: Mapped[int] = mapped_column(ForeignKey("promotion.id"))
    promotion: Mapped[Promotion] = relationship(back_populates="courses")
    duration: Mapped[int] = mapped_column(Integer)
    time_published: Mapped[Date] = mapped_column(
        Date, default=func.current_date(), nullable=False
    )
