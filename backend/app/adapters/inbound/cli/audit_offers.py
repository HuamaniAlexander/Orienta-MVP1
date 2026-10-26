"""Retira de publicación fichas sin alcance geográfico/modalidad documentados; conserva sus datos."""

import json
from pathlib import Path
from urllib.parse import urlsplit

from app.adapters.outbound.persistence.models import Career, Offer
from app.infrastructure.config import get_settings
from app.infrastructure.database import create_database
from sqlalchemy.orm import Session


def audit_offers(session, records, careers=()):
    for review in careers:
        career = session.get(Career, review["career_id"])
        if not career or type(review["active"]) is not bool:
            raise ValueError("Carrera o estado inválido")
        career.active = review["active"]
    for review in records:
        offer = session.get(Offer, review["offer_id"])
        if (
            not offer
            or type(review["active"]) is not bool
            or not review["reason"]
            or urlsplit(review["source_url"]).scheme != "https"
        ):
            raise ValueError("Revisión de alcance inválida")
        offer.active = review["active"]
        offer.detail = {
            **offer.detail,
            "revision_alcance": review["reason"],
            "fuente_revision_alcance": review["source_url"],
            "fecha_revision_alcance": review["reviewed_on"],
        }
    return len(records)


def main():
    engine, _ = create_database(get_settings().database_url)
    with Session(engine) as session, session.begin():
        print(
            "Ofertas auditadas:",
            audit_offers(
                session,
                json.loads(Path("data/auditoria_ofertas.json").read_text()),
                json.loads(Path("data/auditoria_carreras.json").read_text()),
            ),
        )


if __name__ == "__main__":
    main()
