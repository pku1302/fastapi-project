from sqlmodel import Field, SQLModel, Relationship 
from datetime import datetime
from sqlalchemy import Column, DateTime, func
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post
    from .comment import Comment

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)

    email: str | None = Field(default=None, index=True, unique=True)
    hashed_password: str

    comments: List["Comment"] = Relationship(back_populates="user")

    is_active: bool = True
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    ))

    posts: List["Post"] = Relationship(back_populates="user")