from app.models.post import Post

# 글 생성 테스트
def test_create_post(client, created_post, auth_headers):
    data = created_post
    assert data["title"] == "test"

    response = client.post(
        "/posts",
        json={
            "title": "test",
        },
        headers=auth_headers
    )
    assert response.status_code == 422

    response = client.post(
        "/posts",
        json={
            "title": "tteesstt",
            "content": "asdf"
        }
    )

    assert response.status_code == 401

# 글 조회 테스트
def test_read_post(client, created_post):
    post_id = created_post["id"]
    
    response = client.get(f"/posts/{post_id}")
    assert response.json()["id"] == post_id

    response = client.get(f"/posts/{post_id + 1}")
    assert response.status_code == 404

# 글 삭제 테스트
def test_delete_post(client, created_post, auth_headers):
    post_id = created_post["id"]
    
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 401

    response = client.delete(f"/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404

# 삭제된 글은 조회 X, Soft Delete 테스트
def test_deleted_post_not_found(client, session, created_post, auth_headers):
    post_id = created_post["id"]
    client.delete(f"/posts/{post_id}", headers=auth_headers)
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404

    response = client.patch(
        f"/posts/{post_id}",
        json ={
        "title": "updated"
        },
        headers=auth_headers
    )
    assert response.status_code == 404

    post = session.get(Post, post_id)
    assert post is not None
    assert post.deleted_at is not None

# 글 수정 테스트
def test_patch_post(client, created_post, auth_headers):
    post_id = created_post["id"]
    response = client.patch(f"/posts/{post_id}",
         json={
                "title": "updated"
            },
        headers=auth_headers
    )
    data = response.json() 

    assert response.status_code == 200
    assert data["title"] == "updated"
        
    response = client.patch(f"/posts/{post_id}",
         json={
                "content": "updated2"
            },
    )
    assert response.status_code == 401    

