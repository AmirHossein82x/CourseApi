# import databases
# import sqlalchemy
# from courseApi.config import config
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass







# engine = sqlalchemy.create_engine(config.DATABASE_URL)


# Base.metadata.create_all(engine)
# database = databases.Database(
#     config.DATABASE_URL, force_rollback=config.DB_FORCE_ROL_BACK
# )
