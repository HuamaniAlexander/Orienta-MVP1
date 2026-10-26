"""Carga idempotente del directorio documentado. No altera carreras ni ofertas."""

import json
from pathlib import Path
from urllib.parse import urlsplit

from app.adapters.outbound.persistence.models import DirectoryInstitution
from app.infrastructure.config import get_settings
from app.infrastructure.database import create_database
from sqlalchemy.orm import Session


def validate_directory(records):
    slugs = set()
    for item in records:
        if item["slug"] in slugs or not item["locations"]:
            raise ValueError("Institución duplicada o sin ubicación")
        slugs.add(item["slug"])
        for url in (item["website"], *[s["url"] for s in item["sources"]]):
            if urlsplit(url).scheme != "https" or not urlsplit(url).hostname:
                raise ValueError("Las fuentes deben ser HTTPS")
        if not item["sources"] or not item["reviewed_on"]:
            raise ValueError("Falta trazabilidad")
    return records


def import_directory(session, records):
    for item in validate_directory(records):
        session.merge(
            DirectoryInstitution(slug=item["slug"], name=item["name"], kind=item["kind"], data=item)
        )
    return len(records)


def main():
    records = json.loads(Path("data/instituciones_lima_norte.json").read_text())
    engine, _ = create_database(get_settings().database_url)
    with Session(engine) as session, session.begin():
        print(f"Instituciones cargadas: {import_directory(session, records)}")


if __name__ == "__main__":
    main()
