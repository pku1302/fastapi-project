from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, DateTime, func
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .user import User
    from .comment import Comment

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    content: str
    author_name: str | None = None
    comment_count: int = Field(
        default=0,
        sa_column_kwargs={"server_default": "0"}
        )

    user_id: str = Field(
        foreign_key="user.id",
        index=True,
    )

    comments: List["Comment"] = Relationship(back_populates="post")

    user: Optional["User"] = Relationship(back_populates="posts")

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    ))

    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now(),
    ))
    
    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(
        DateTime(timezone=True),
        nullable=True
    ))
