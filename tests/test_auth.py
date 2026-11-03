def register(client, email="User@Example.com"):
    return client.post(
        "/api/auth/register",
        json={"email": email, "password": "correct-horse-battery"},
    )


def test_register_login_and_current_user(client):
    registered = register(client)
    assert registered.status_code == 201
    assert registered.json()["email"] == "user@example.com"

    login = client.post(
        "/api/auth/login",
        json={"email": "USER@example.com", "password": "correct-horse-battery"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    current_user = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert current_user.status_code == 200
    assert current_user.json()["email"] == "user@example.com"


def test_duplicate_registration_is_rejected(client):
    assert register(client).status_code == 201

    duplicate = register(client, "user@example.com")

    assert duplicate.status_code == 409


def test_protected_route_requires_valid_credentials(client):
    missing = client.get("/api/auth/me")
    invalid = client.get(
        "/api/auth/me", headers={"Authorization": "Bearer invalid-token"}
    )

    assert missing.status_code == 401
    assert invalid.status_code == 401


def test_login_rejects_wrong_password(client):
    assert register(client).status_code == 201

    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
