import databases
import sqlalchemy
from courseApi.config import config
from courseApi.models.base import Base
from .user import User  # noqa: F401


engine = sqlalchemy.create_engine(config.DATABASE_URL)


Base.metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROL_BACK
)
