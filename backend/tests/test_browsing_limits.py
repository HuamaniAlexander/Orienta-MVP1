def test_browsing_session_does_not_exhaust_sign_in_budget(client):
    for _ in range(35):
        assert client.get("/api/v1/auth/me").status_code == 401
    token = client.get("/api/v1/auth/csrf").json()["csrf_token"]
    response = client.post(
        "/api/v1/auth/registro",
        json={"email": "browse@example.com", "password": "una-frase-segura-2026"},
        headers={"X-CSRF-Token": token},
    )
    assert response.status_code == 201
