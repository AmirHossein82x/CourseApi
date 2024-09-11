import databases
import sqlalchemy
from courseApi.config import config

meta_data = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(config.DATABASE_URL)


meta_data.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROL_BACK
)
