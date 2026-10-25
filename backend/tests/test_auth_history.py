from uuid import uuid4

from app.adapters.outbound.persistence.models import Comparison, Feedback, User
from conftest import csrf, login
from fastapi.testclient import TestClient
from sqlalchemy import select


def test_password_hash_and_cookie_security(client, seeded):
    login(client)
    with seeded[1]() as session:
        user = session.scalar(select(User))
        assert user.password_hash.startswith("$argon2id$")
        assert "mi-frase" not in user.password_hash
    response = client.get("/api/v1/auth/csrf")
    assert (
        "HttpOnly" in response.headers["set-cookie"]
        and "SameSite=lax" in response.headers["set-cookie"]
    )
    assert client.get("/api/v1/auth/me").json()["email"] == "alumno@example.com"


def test_csrf_and_origin_are_required(client):
    body = {"email": "alumno@example.com", "password": "mi-frase-segura-2026"}
    assert client.post("/api/v1/auth/registro", json=body).status_code == 403
    headers = {**csrf(client), "Origin": "https://malicioso.example"}
    assert client.post("/api/v1/auth/registro", json=body, headers=headers).status_code == 403


def test_login_rotates_and_logout_revokes(client):
    login(client)
    token = client.cookies.get("orienta_session")
    response = client.post("/api/v1/auth/logout", headers=csrf(client))
    assert response.status_code == 204
    assert client.get("/api/v1/auth/me").status_code == 401
    client.cookies.set("orienta_session", token)
    assert client.get("/api/v1/auth/me").status_code == 401


def test_private_history_idempotency_and_delete(client, payload, seeded):
    login(client)
    payload["catalog_version"] = client.post("/api/v1/recomendaciones", json=payload).json()[
        "catalog_version"
    ]
    key = str(uuid4())
    headers = {**csrf(client), "Idempotency-Key": key}
    saved = client.post("/api/v1/comparaciones", json=payload, headers=headers)
    assert saved.status_code == 201, saved.text
    cid = saved.json()["id"]
    repeated = client.post(
        "/api/v1/comparaciones", json=payload, headers={**csrf(client), "Idempotency-Key": key}
    )
    assert repeated.json()["id"] == cid
    assert client.get("/api/v1/comparaciones").json()["total"] == 1
    payload["responses"]["Q01"] = 1
    conflict = client.post(
        "/api/v1/comparaciones", json=payload, headers={**csrf(client), "Idempotency-Key": key}
    )
    assert conflict.status_code == 409
    with TestClient(client.app) as other:
        login(other, "otro@example.com")
        assert other.get("/api/v1/comparaciones/" + cid).status_code == 404
        assert other.delete("/api/v1/comparaciones/" + cid, headers=csrf(other)).status_code == 404
    assert (
        client.post(
            f"/api/v1/comparaciones/{cid}/feedback", json={"score": 4}, headers=csrf(client)
        ).status_code
        == 201
    )
    assert client.delete("/api/v1/comparaciones/" + cid, headers=csrf(client)).status_code == 204
    with seeded[1]() as session:
        assert session.scalar(select(Comparison)) is None
        assert session.scalar(select(Feedback)) is None


def test_guest_history_denied(client):
    assert client.get("/api/v1/comparaciones").status_code == 401


def test_rate_limit_auth(client):
    for _ in range(30):
        client.get("/api/v1/auth/me")
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 429 and response.headers["Retry-After"] == "60"
