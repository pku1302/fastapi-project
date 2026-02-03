from app.schemas.post_schema import PostCreate, PostUpdate, PostResponse, PostListResponse
from sqlmodel import select, desc, func
from datetime import datetime
from app.models.post import Post
from app.models.comment import Comment

SORT_MAP = {
    "created_at": Post.created_at
}

# 글 조회 공통함수
def get_active_post(session, post_id: int):
    return session.exec(
        select(Post)
        .where(Post.id == post_id)
        .where(Post.deleted_at.is_(None))
    ).first()

# 글 생성
def create_post(post: PostCreate, user_id: str, session) -> Post:
    db_post = Post(
        **post.model_dump(),
        user_id = user_id
    )
    
    session.add(db_post)
    session.commit()
    session.refresh(db_post)

    return db_post

# 글 페이지네이션 조회
def get_posts(session, offset, limit, sort, order 
              ) -> tuple[int, list[PostResponse]]:
    sort_column = SORT_MAP.get(sort, Post.created_at)
    order_by = desc(sort_column)

    total = session.exec(
        select(func.count())
        .select_from(Post)
        .where(Post.deleted_at.is_(None))
    ).one()

    stmt = (
        select(Post)
        .where(Post.deleted_at.is_(None))
        .order_by(order_by)
        .offset(offset)
        .limit(limit)
    )

    posts = session.exec(stmt).all()
    total = int(total)
    return total, posts

# 단일 글 조회
def get_post(session, post_id):
    post = get_active_post(session, post_id)

    if not post:
        return None

    comments = session.exec(
        select(Comment)
        .where(Comment.post_id == post_id)
    ).all()

    for c in comments:
        if c.is_deleted:
            c.content = "삭제된 댓글입니다."

    post.comments = comments

    return post
    
# 글 수정
def update_post(session, post_id: int, post: PostUpdate):
    post_db = get_active_post(session, post_id)

    if not post_db:
        return None
    
    post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_data)

    session.add(post_db)
    session.commit()
    session.refresh(post_db)

    return post_db

# 글 삭제
def delete_post(session, post_id):
    post = get_active_post(session, post_id)

    if not post:
        return None
    
    post.deleted_at = datetime.now()
    session.add(post)
    session.commit()

    return {"ok": True}