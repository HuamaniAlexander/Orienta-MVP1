"""Publica perfiles preparados y revisados por responsables académicos."""

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

from app.adapters.outbound.persistence.models import Career
from app.domain.errors import DomainError
from app.infrastructure.config import get_settings
from app.infrastructure.database import create_database


def publish_profiles(session, records):
    validated = []
    for item in records:
        profile = item.get("profile", [])
        if len(profile) != 6 or any(
            type(v) not in (int, float) or not 0 <= v <= 1 for v in profile
        ):
            raise DomainError("Cada perfil necesita seis valores entre 0 y 1")
        if (
            len(set(item.get("reviewers", []))) < 2
            or not item.get("sources")
            or not item.get("rubric_version")
        ):
            raise DomainError("Se requieren dos revisores, fuentes y versión de rúbrica")
        date.fromisoformat(item["reviewed_at"])
        career = session.get(Career, item["career_id"])
        if not career:
            raise DomainError("Carrera desconocida")
        validated.append((career, item))
    for career, item in validated:
        career.profile = item["profile"]
        career.profile_reviewed = True
        career.content = {**career.content, "academic_review": item}
        career.version = hashlib.sha256(json.dumps(item, sort_keys=True).encode()).hexdigest()[:12]
    session.flush()
    return len(validated)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    engine, factory = create_database(get_settings().database_url)
    try:
        with factory.begin() as session:
            count = publish_profiles(session, json.loads(args.path.read_text()))
        print(f"Perfiles revisados publicados: {count}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
