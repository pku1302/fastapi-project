from datetime import datetime
from app.models.post import Post
from app.models.comment import Comment

def create_post(
    *,
    title: str,
    created_at: datetime,
    deleted_at: datetime | None = None,
    user_id: str,
):
    return Post(
        title=title,
        content="test",
        created_at=created_at,
        deleted_at=deleted_at,
        user_id = user_id
    )

