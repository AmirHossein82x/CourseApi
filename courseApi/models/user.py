from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, sql


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(60))
    is_admin:Mapped[bool] = mapped_column(Boolean, server_default=sql.expression.false(), default=sql.expression.false())
