from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import List

class CommentCreate(SQLModel):
    content: str
    parent_id: int | None = None

class CommentRead(SQLModel):
    id: int
    content: str
    post_id: int
    user_id: str
    parent_id: int | None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

class CommentUpdate(SQLModel):
    content: str
    
class CommentReadWithChildren(SQLModel):
    id: int
    content: str
    user_id: str
    parent_id: int | None
    created_at: datetime
    children: List["CommentReadWithChildren"] = []


