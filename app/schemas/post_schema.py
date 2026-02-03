from datetime import datetime
from sqlmodel import SQLModel, Field
from app.models.post import Post
from app.schemas.comment_schema import CommentRead

# API용, 클라이언트를 위한 데이터 모델
class PostBase(SQLModel):
    title: str = Field(max_length=100, index=True)
    content: str

# 글 생성 모델
class PostCreate(PostBase):
    pass

# 단일 글 반환 모델
class PostResponse(PostBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    user_id: str
    comments: list[CommentRead]

# 수정 글 모델
class PostUpdate(PostBase):
    title: str | None = Field(default=None, max_length=100)
    content: str | None = None
    
# 글 삭제 모델
class PostDelete(SQLModel):
    user_id: str


# 글 리스트 반환 모델 중 글 하나
class PostListOne(PostBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    user_id: str
    comment_count: int

# 글 리스트 반환 모델
class PostListResponse(SQLModel):
    total: int
    posts: list[PostListOne]