import json
import os
from pathlib import Path
from uuid import uuid4

import pytest
from app.adapters.outbound.persistence.importer import SqlCatalogImporter
from app.adapters.outbound.persistence.models import Base
from app.application.importation.use_cases import import_catalog
from app.infrastructure.config import Settings
from fastapi.testclient import TestClient
from main import create_app
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def records():
    return json.loads((ROOT / "data/catalogo_legacy.json").read_text())


@pytest.fixture
def editorial():
    return json.loads((ROOT / "data/contenido_editorial.json").read_text())


@pytest.fixture
def database():
    url = os.getenv("TEST_DATABASE_URL")
    schema = "orienta_test_" + uuid4().hex[:12]
    if url:
        base = create_engine(url, hide_parameters=True)
        with base.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = base.execution_options(schema_translate_map={"orienta": schema})
    else:
        base = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )

        @event.listens_for(base, "connect")
        def enable_fk(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")

        engine = base.execution_options(schema_translate_map={"orienta": None})
    Base.metadata.create_all(engine)
    yield engine, sessionmaker(engine, expire_on_commit=False)
    if url:
        with base.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
    base.dispose()


@pytest.fixture
def seeded(database, records, editorial):
    with database[1].begin() as session:
        import_catalog(SqlCatalogImporter(session), records, editorial)
    return database


@pytest.fixture
def client(seeded):
    app = create_app(
        Settings(_env_file=None, demo_mode=True, gemini_api_key="", gemini_model=""), seeded
    )
    with TestClient(app) as value:
        yield value


@pytest.fixture
def payload():
    return {
        "career_ids": [0, 1],
        "questionnaire_version": "q1",
        "responses": {f"Q{i:02}": 4 for i in range(1, 9)},
        "conditions": {"monthly_budget": 800},
    }


def csrf(client):
    return {"X-CSRF-Token": client.get("/api/v1/auth/csrf").json()["csrf_token"]}


def login(client, email="alumno@example.com"):
    body = {"email": email, "password": "mi-frase-segura-2026"}
    assert client.post("/api/v1/auth/registro", json=body, headers=csrf(client)).status_code == 201
    assert client.post("/api/v1/auth/login", json=body, headers=csrf(client)).status_code == 200
