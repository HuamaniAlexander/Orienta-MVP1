"""Demo local explícita: SQLite y perfiles editoriales ilustrativos, nunca producción."""

import json
from pathlib import Path

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
    return create_app(Settings(demo_mode=True, database_url="sqlite:///demo.db"), (engine, factory))
