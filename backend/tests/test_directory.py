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
    assert data["total"] == len(records())
    assert len({i["slug"] for i in data["items"]}) == len(records())
    assert {
        "Comas",
        "Los Olivos",
        "Independencia",
        "San Martín de Porres",
        "Rímac",
        "Puente Piedra",
    } == {location["district"] for i in data["items"] for location in i["locations"]}
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


def test_official_registry_coverage_is_complete_for_the_published_snapshot():
    registry = json.loads(Path("data/padron_minedu_norte.json").read_text())
    expected = {r["code"] for r in registry["institutions"]}
    covered = {i.get("modular_code") for i in records()}
    assert len(expected) == 17 and expected <= covered


def test_programs_import_and_institution_detail_preserve_cost_scope(client, seeded):
    from app.adapters.inbound.cli.import_programs import import_programs
    from app.adapters.outbound.persistence.models import Career

    programs = json.loads(Path("data/programas_institucionales.json").read_text())
    technical = json.loads(Path("data/carreras_tecnicas.json").read_text())
    with seeded[1].begin() as session:
        import_directory(session, records())
        import_programs(session, programs, technical)
        session.flush()
        version = session.get(Career, 0).version
        import_programs(session, programs, technical)
        assert session.get(Career, 0).version == version
    detail = client.get("/api/v1/directorio/instituciones/uch").json()
    assert len(detail["academic_programs"]) == 8
    systems = next(p for p in detail["academic_programs"] if p["career_id"] == 0)
    assert systems["tuition"]["min"] == 720
    assert "matrícula" in systems["tuition"]["scope"]
    assert client.get("/api/v1/carreras/11").json()["kind"] == "tecnica"
    assert client.get("/api/v1/carreras/11").json()["comparison"]["duration"] == "3 años"


def test_audit_archives_unbacked_offers_without_deleting_them(seeded):
    from app.adapters.inbound.cli.audit_offers import audit_offers
    from app.adapters.outbound.persistence.models import Offer
    from sqlalchemy import func, select

    with seeded[1].begin() as session:
        audit_offers(session, json.loads(Path("data/auditoria_ofertas.json").read_text()))
        assert session.scalar(select(func.count()).select_from(Offer)) == 19
        assert (
            session.scalar(select(func.count()).select_from(Offer).where(Offer.active.is_(False)))
            == 8
        )
