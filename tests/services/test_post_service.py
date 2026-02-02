from datetime import datetime, timedelta
from app.services import post_service
from tests.helpers.post_factory import create_post
from app.models.user import User

# total count 테스트
def test_get_posts_basic(session):
    now = datetime.now()

    user = User(
        id="testuser",
        hashed_password="x"
    )

    session.add(user)

    session.add_all([
        create_post(
            title= "a",
            created_at= now,
            user_id = user.id
        ),
        create_post(
            title= "b",
            created_at= now,
            user_id = user.id
        ),
        create_post(
            title= "c",
            created_at= now,
            user_id = user.id
        )
    ])

    session.commit()

    total, posts = post_service.get_posts(
        session=session,
        offset=0,
        limit=10,
        sort="created_at",
        order="desc"
    )

    assert total == 3
    assert len(posts) == 3

# 소프트 삭제 
def test_get_posts_excludes_soft_deleted(session):
    now = datetime.now()

    user = User(
        id="testuser",
        hashed_password="x"
    )

    session.add(user)

    alive = create_post(
        title= "alive",
        created_at= now,
        user_id=user.id
    )

    deleted = create_post(
        title= "deleted",
        created_at= now,
        deleted_at= now,
        user_id=user.id
    )

    session.add_all([alive, deleted])
    session.commit()

    total, posts = post_service.get_posts(
        session=session,
        offset=0,
        limit=10,
        sort="created_at",
        order="desc"
    )

    assert total == 1
    assert posts[0].title == "alive"

# 정렬 검증
def test_get_posts_sorted_desc(session):
    now = datetime.now()

    user = User(
        id="testuser",
        hashed_password="x"
    )

    session.add(user)

    session.add_all([
        create_post(title="old", created_at=now - timedelta(days=2), user_id=user.id),
        create_post(title="mid", created_at=now - timedelta(days=1), user_id=user.id),
        create_post(title="new", created_at=now, user_id=user.id),
    ])
    session.commit()

    _, posts = post_service.get_posts(
        session=session,
        offset=0,
        limit=10,
        sort="created_at",
        order="desc",
    )

    titles=[p.title for p in posts]
    assert titles == ["new", "mid", "old"]

# 페이지네이션 검증
def test_get_posts_pagination(session):
    now = datetime.now()

    user = User(
        id="testuser",
        hashed_password="x"
    )

    session.add(user)

    for i in range(5):
        session.add(
            create_post(
                title=f"post{i}",
                created_at=now - timedelta(minutes=i),
                user_id = user.id
            )
        )
    session.commit()

    _, posts = post_service.get_posts(
        session=session,
        offset=2,
        limit=2,
        sort="created_at",
        order="desc",
    )

    assert len(posts) == 2

# 잘못된 sort -> fallback
def test_get_posts_invalid_sort_fallback(session):
    now = datetime.now()

    user = User(
        id="testuser",
        hashed_password="x"
    )

    session.add(user)

    session.add_all([
        create_post(title="a", created_at=now, user_id=user.id),
        create_post(title="b", created_at=now - timedelta(days=1), user_id=user.id),
    ])
    session.commit()

    _, posts = post_service.get_posts(
        session=session,
        offset=0,
        limit=10,
        sort="invalid",
        order="desc"
    )

    titles = [p.title for p in posts]
    assert titles == ["a", "b"]