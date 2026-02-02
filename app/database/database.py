from typing import Annotated
from sqlmodel import create_engine, Session
from fastapi import Depends

from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]