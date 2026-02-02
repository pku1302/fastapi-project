def test_login_success(client, created_user):
    response = client.post(
        "/token",
        data={
            "username": created_user["id"],
            "password": "testpassword"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_login_fail(client):
    response = client.post(
        "/token",
        data={
            "username": "wrongid",
            "password": "wrongpw",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    assert response.status_code == 401

def test_auth_required_without_token(client):
    response = client.get("/protected")
    assert response.status_code == 401

def test_auth_required_with_token(client, created_user):
    login = client.post(
        "/token",
        data={
            "username": created_user["id"],
            "password": "testpassword"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.get(
        "/protected",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == created_user["id"]