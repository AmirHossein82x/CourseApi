from contextlib import asynccontextmanager
from courseApi.models import database
from fastapi import FastAPI
from courseApi.routers.user import router as userRouter
from courseApi.routers.course import router as courseRouter
from courseApi.routers.buy_course import router as buyCourseRouter
from courseApi.logging_conf import configure_logging
from asgi_correlation_id import CorrelationIdMiddleware
import logging


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(userRouter)
app.include_router(courseRouter)
app.include_router(buyCourseRouter)

