from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from sqlalchemy import Column, DateTime, func

if TYPE_CHECKING:
    from .user import User
    from .post import Post

class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)

    content: str

    post_id: int = Field(foreign_key="post.id")
    user_id: str = Field(foreign_key="user.id")

    post: Optional["Post"] = Relationship(back_populates="comments")
    user: Optional["User"] = Relationship(back_populates="comments")

    parent_id: Optional[int] = Field(
        default=None,
        foreign_key="comments.id"
    )

    is_deleted: bool = Field(default=False)

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()
        )
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now()
        )
    )

    parent: Optional["Comment"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Comment.id"},
    )

    children: List["Comment"] = Relationship(
        back_populates="parent"
    )