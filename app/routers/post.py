from typing import Annotated
from fastapi import APIRouter, Query, HTTPException, Path, Depends
from app.schemas.post_schema import PostResponse, PostCreate, PostUpdate, PostListResponse, PostDelete
from app.models.post import Post
from app.models.user import User
from app.database.database import SessionDep
from app.services import post_service
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])

# 글 작성
@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, session: SessionDep, current_user: User = Depends(get_current_user)) -> Post:
    db_post = post_service.create_post(post, current_user.id, session)
    return db_post

# 글 조회, 페이지네이션, 정렬
@router.get("/", response_model = PostListResponse)
def read_posts(
    session: SessionDep,
    *,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=20)] = 20,
    sort: Annotated[str, Query()] = "created_at", 
    order: Annotated[str, Query()] = "desc"
):
    total, posts = post_service.get_posts(session, offset, limit, sort, order)
    return {
        "total": total,
        "posts": posts
    }

# 특정 글 조회
@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: Annotated[int, Path()], 
              session: SessionDep):
    post = post_service.get_post(session, post_id)
    if not post:
         raise HTTPException(status_code=404, detail="Post Not Found")
    return post

# 특정 글 수정
@router.patch("/{post_id}", response_model=PostResponse)
def update_post(post_id: Annotated[int, Path()],
                 update_post: PostUpdate,
                 session: SessionDep,
                 current_user: User = Depends(get_current_user), 
                 ):
    db_post = session.get(Post, post_id)
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한없음")
    
    updated = post_service.update_post(session, post_id, update_post)
    if not updated:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return updated

# 특정 글 삭제
# Soft delete를 적용합니다.
@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: Annotated[int, Path()], 
                session: SessionDep,
                current_user: User = Depends(get_current_user)
                ):
    post = session.get(Post, post_id)
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한없음")
    
    if not post_service.delete_post(session, post_id):
        raise HTTPException(status_code=404, detail="Post Not Found")