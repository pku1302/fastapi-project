from datetime import datetime
from app.models.user import User

def test_comment(client, created_post, auth_headers):
    post_id = created_post["id"]
    response = client.post(
        f"/comments/{post_id}",
        json={
            "content": "test"
        },
        headers=auth_headers
    )
    comment_id = response.json()["id"]

    assert response.status_code == 200

    response = client.post(
        f"posts",
        json={
            "title": "test",
            "content": "asdf"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    another_post_id = response.json()["id"]
    response = client.post(
        f"/comments/{another_post_id}",
        json={
            "content": "another",
            "parent_id": f"{comment_id}"
        },
        headers=auth_headers
    )

    assert response.status_code == 400

    response = client.post(
        f"/comments/{post_id}",
        json={
            "content": "test"
        },
    )

    assert response.status_code == 401

    response = client.patch(
        f"/comments/{comment_id}",
        json={
            "content": "updated"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["content"] == "updated"

    client.post(
        f"/signup",
        json={
            "id": "another",
            "password": "testpassword",
        }
    )
    response = client.post(
        f"/token",
        data={
            "username": "another",
            "password": "testpassword"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.patch(
        f"/comments/{comment_id}",
        json={
            "content": "another update"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 403

    response = client.delete(
        f"/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403

    response = client.delete(
        f"/comments/{comment_id}",
        headers=auth_headers
    )

    assert response.status_code == 204

