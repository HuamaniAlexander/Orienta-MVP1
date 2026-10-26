"""Demo local explícita: SQLite y perfiles editoriales ilustrativos, nunca producción."""

import json
from pathlib import Path

from app.adapters.inbound.cli.audit_offers import audit_offers
from app.adapters.inbound.cli.import_directory import import_directory
from app.adapters.inbound.cli.import_programs import import_programs
from app.adapters.inbound.cli.review_offers import review_offers
from app.adapters.outbound.persistence.importer import import_catalog_sql
from app.adapters.outbound.persistence.models import Base
from app.infrastructure.config import Settings
from main import create_app
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker


def make_app():
    engine = create_engine(
        "sqlite:///demo.db",
        connect_args={"check_same_thread": False},
        execution_options={"schema_translate_map": {"orienta": None}},
    )

    @event.listens_for(engine, "connect")
    def foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    with factory.begin() as session:
        import_catalog_sql(
            session,
            json.loads(Path("data/catalogo_legacy.json").read_text()),
            json.loads(Path("data/contenido_editorial.json").read_text()),
        )
        import_directory(
            session, json.loads(Path("data/instituciones_lima_norte.json").read_text())
        )
        review_offers(session, json.loads(Path("data/revisiones_ofertas.json").read_text()))
        import_programs(
            session,
            json.loads(Path("data/programas_institucionales.json").read_text()),
            json.loads(Path("data/carreras_tecnicas.json").read_text()),
        )
        audit_offers(
            session,
            json.loads(Path("data/auditoria_ofertas.json").read_text()),
            json.loads(Path("data/auditoria_carreras.json").read_text()),
        )
    return create_app(
        Settings(
            _env_file=None,
            demo_mode=True,
            database_url="sqlite:///demo.db",
            gemini_api_key="",
            gemini_model="",
        ),
        (engine, factory),
    )
