"""Carga planes institucionales con precios y documentos trazables."""

import json
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlsplit

from app.adapters.outbound.persistence.models import (
    Career,
    DirectoryInstitution,
    InstitutionalProgram,
)
from app.infrastructure.config import get_settings
from app.infrastructure.database import create_database
from sqlalchemy.orm import Session


def import_programs(session, records, careers=()):
    for item in careers:
        if not session.get(Career, item["code"]):
            session.add(
                Career(
                    **item, profile=None, profile_reviewed=False, active=True, version="tecnica-1"
                )
            )
    session.flush()
    seen = set()
    for item in records:
        if (
            item["id"] in seen
            or not session.get(DirectoryInstitution, item["institution_slug"])
            or not session.get(Career, item["career_id"])
        ):
            raise ValueError("Programa duplicado o referencia inexistente")
        seen.add(item["id"])
        urls = [item["source_url"]] + [d["url"] for d in item.get("documents", [])]
        if any(urlsplit(url).scheme != "https" or not urlsplit(url).hostname for url in urls):
            raise ValueError("Fuente no HTTPS")
        tuition = item.get("tuition")
        if tuition:
            lo, hi = Decimal(str(tuition["min"])), Decimal(str(tuition["max"]))
            if (
                not lo.is_finite()
                or not hi.is_finite()
                or lo < 0
                or hi < lo
                or not tuition.get("scope")
                or not tuition.get("period")
            ):
                raise ValueError("Tarifa sin alcance, periodo o rango válido")
        session.merge(
            InstitutionalProgram(
                id=item["id"],
                institution_slug=item["institution_slug"],
                career_code=item["career_id"],
                data=item,
            )
        )
    return len(seen)


def main():
    engine, _ = create_database(get_settings().database_url)
    with Session(engine) as session, session.begin():
        print(
            "Programas cargados:",
            import_programs(
                session,
                json.loads(Path("data/programas_institucionales.json").read_text()),
                json.loads(Path("data/carreras_tecnicas.json").read_text()),
            ),
        )


if __name__ == "__main__":
    main()
