"""Aplica revisiones de precios con fuente y periodo sin modificar el archivo legado."""

import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlsplit

from app.adapters.outbound.persistence.models import Career, Offer
from app.infrastructure.config import get_settings
from app.infrastructure.database import create_database
from sqlalchemy.orm import Session


def review_offers(session, records):
    seen = set()
    changed = {}
    for review in records:
        source = urlsplit(review["source"])
        cost = Decimal(str(review["cost"]))
        if (
            review["offer_id"] in seen
            or not cost.is_finite()
            or cost < 0
            or source.scheme != "https"
            or not source.hostname
            or not all(review.get(k) for k in ("period", "scope", "reviewed_on", "district"))
        ):
            raise ValueError("Revisión incompleta, costo inválido o identificador duplicado")
        seen.add(review["offer_id"])
        offer = session.get(Offer, review["offer_id"])
        if not offer:
            raise ValueError("La oferta debe existir antes de revisarla")
        offer.cost, offer.cost_min, offer.cost_max = cost, None, None
        offer.district, offer.cost_status = review["district"], "verificado"
        offer.detail = {
            **offer.detail,
            "fuente_costo": review["source"],
            "estado_costo": review["scope"],
            "periodo_costo": review["period"],
            "fecha_revision_costo": review["reviewed_on"],
        }
        changed.setdefault(offer.career_code, []).append(review)
    for code, reviews in changed.items():
        career = session.get(Career, code)
        digest = hashlib.sha256(json.dumps(reviews, sort_keys=True).encode()).hexdigest()[:12]
        career.version = career.version.split("-rev-", 1)[0][:40] + "-rev-" + digest
    return len(seen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    engine, _ = create_database(get_settings().database_url)
    with Session(engine) as session, session.begin():
        print(f"Ofertas revisadas: {review_offers(session, json.loads(args.path.read_text()))}")


if __name__ == "__main__":
    main()
