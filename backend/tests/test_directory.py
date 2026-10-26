import json
from pathlib import Path

import pytest
from app.adapters.inbound.cli.import_directory import import_directory, validate_directory


def records():
    return json.loads(Path("data/instituciones_lima_norte.json").read_text())


def test_directory_is_idempotent_and_not_an_academic_offer(client, database):
    with database[1].begin() as session:
        import_directory(session, records())
        import_directory(session, records())
    response = client.get("/api/v1/directorio/instituciones")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 17
    assert len({i["slug"] for i in data["items"]}) == 17
    assert {"Comas", "Los Olivos", "Independencia", "San Martín de Porres", "Rímac"} == {
        location["district"] for i in data["items"] for location in i["locations"]
    }
    assert client.get("/api/v1/ofertas").json()["items"]


def test_directory_rejects_unsafe_links_and_duplicates():
    data = records()
    data[0]["website"] = "javascript:alert(1)"
    with pytest.raises(ValueError):
        validate_directory(data)
    with pytest.raises(ValueError):
        validate_directory([records()[0], records()[0]])


def test_reviewed_prices_keep_legacy_file_and_are_idempotent(seeded):
    from app.adapters.inbound.cli.review_offers import review_offers
    from app.adapters.outbound.persistence.models import Career, Offer

    reviews = json.loads(Path("data/revisiones_ofertas.json").read_text())
    original = Path("data/catalogo_legacy.json").read_bytes()
    with seeded[1].begin() as session:
        review_offers(session, reviews)
        session.flush()
        version = session.get(Career, 0).version
        review_offers(session, reviews)
        assert session.get(Career, 0).version == version
        offer = session.get(Offer, "C01")
        assert offer.cost == 815 and offer.district == "Los Olivos"
        assert offer.cost_status == "verificado"
        assert offer.detail["periodo_costo"] == "2026 · agosto"
    assert Path("data/catalogo_legacy.json").read_bytes() == original
