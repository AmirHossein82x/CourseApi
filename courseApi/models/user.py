from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(60))
