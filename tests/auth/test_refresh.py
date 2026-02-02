def test_refresh_flow(client, created_user):
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

    tokens = response.json()
    refresh_token = tokens["refresh_token"]

    refresh_res = client.post(
        "/token/refresh",
        json={"refresh_token": refresh_token}
    )

    assert refresh_res.status_code == 200

    new_access_token = refresh_res.json()["access_token"]

    protected_res = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )

    assert protected_res.status_code == 200