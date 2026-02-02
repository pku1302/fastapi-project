from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import post, signup, login,protected
from app.database.database import engine
from sqlmodel import SQLModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    #SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(signup.router)
app.include_router(login.router)
app.include_router(protected.router)

@app.get("/")
async def root():
    return {"message": "Hello"}