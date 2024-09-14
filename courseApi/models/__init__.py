import databases
import sqlalchemy
from courseApi.config import config
from .user import User  # noqa: F401
from .course import Course, Promotion  # noqa: F401
from .base import Base # noqa: F401


engine = sqlalchemy.create_engine(config.DATABASE_URL)


# Base.metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROL_BACK
)
