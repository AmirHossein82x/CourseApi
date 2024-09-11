from fastapi import FastAPI
from contextlib import asynccontextmanager
from courseApi.models import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield 
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
@app.get("/")
async def show():
    return {"ping": "pong"}