from contextlib import asynccontextmanager
from courseApi.models import database
from fastapi import FastAPI
from courseApi.routers.user import router as userRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(userRouter)


@app.get("/")
async def show():
    return {"ping": "pong"}
