from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import select

from app.services.comment_service import build_comment_tree

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment

from app.schemas.comment_schema import CommentRead, CommentCreate, CommentUpdate, CommentReadWithChildren
from app.database.database import SessionDep
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/{post_id}", response_model=CommentRead)
def create_comment(
    post_id: Annotated[int, Path()],
    data: CommentCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    
    if data.parent_id:
        parent = session.get(Comment, data.parent_id)

        if not parent:
            raise HTTPException(404, "Parent comment not found")
        
        if parent.post_id != post_id:
            raise HTTPException(400, "Parent comment does not belong to this post")
    
    comment = Comment(
        content=data.content,
        post_id=post_id,
        parent_id=data.parent_id,
        user_id=current_user.id
    )

    post.comment_count += 1

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment

@router.get("/{post_id}", response_model=list[CommentReadWithChildren])
def get_comment_tree(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)

    if not post or post.deleted_at:
        raise HTTPException(404, "Post not found")
    
    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at)
    )

    comments = session.exec(statement).all()

    return build_comment_tree(comments)

@router.patch("/{comment_id}", response_model=CommentRead)
def update_comment(
    comment_id: int,
    data: CommentUpdate,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    comment = session.get(Comment, comment_id)

    if not comment or comment.is_deleted:
        raise HTTPException(404, "Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(403, "No permission")
    
    comment.content = data.content

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment

@router.delete("/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    comment = session.get(Comment, comment_id)

    if not comment or comment.is_deleted:
        raise HTTPException(404, "Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(403, "No permission")
    
    comment.is_deleted = True

    session.add(comment)
    session.commit()