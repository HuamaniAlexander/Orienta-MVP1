import copy

import pytest
from app.adapters.outbound.persistence.importer import SqlCatalogImporter
from app.adapters.outbound.persistence.models import Career, ImportBatch, LegacyCode, Offer
from app.application.importation.use_cases import import_catalog
from app.domain.errors import DomainError
from sqlalchemy import func, select


def test_import_preserves_codes_and_is_idempotent(seeded, records, editorial):
    with seeded[1].begin() as session:
        report = import_catalog(SqlCatalogImporter(session), records, editorial)
        assert report["unchanged"] is True
        assert session.scalar(select(func.count()).select_from(Offer)) == 19
        assert session.scalar(select(func.count()).select_from(Career)) == 11
        assert session.get(Offer, "C01").legacy_code == 0
        assert session.get(Offer, "C19").legacy_code == 18
        assert session.get(LegacyCode, ("institucion", 1)).value == "UNMSM"
        assert session.scalar(select(func.count()).select_from(ImportBatch)) == 1


def test_historical_remapping_rejected(seeded, records, editorial):
    modified = copy.deepcopy(records)
    for row in modified:
        row["institucion_codigo"] = 1 - row["institucion_codigo"]
    with seeded[1].begin() as session, pytest.raises(DomainError, match="reasignar"):
        import_catalog(SqlCatalogImporter(session), modified, editorial)


def test_dry_run_does_not_write(database, records, editorial):
    with database[1].begin() as session:
        import_catalog(SqlCatalogImporter(session), records, editorial, True)
        assert session.scalar(select(func.count()).select_from(Offer)) == 0


def test_transaction_rolls_back_on_intermediate_failure(database, records, editorial, monkeypatch):
    with pytest.raises(RuntimeError):
        with database[1].begin() as session:
            flush = session.flush
            count = 0

            def failing_flush(*args, **kwargs):
                nonlocal count
                count += 1
                if count > 8:
                    raise RuntimeError("fallo simulado")
                return flush(*args, **kwargs)

            monkeypatch.setattr(session, "flush", failing_flush)
            import_catalog(SqlCatalogImporter(session), records, editorial)
    with database[1]() as session:
        assert session.scalar(select(func.count()).select_from(Offer)) == 0
        assert session.scalar(select(func.count()).select_from(LegacyCode)) == 0


def test_catalog_and_filters_are_combined(client):
    result = client.get("/api/v1/carreras", params={"q": "Sistemas", "area": "Ingeniería"})
    assert result.status_code == 200
    assert result.json()["total"] == 1
    assert client.get("/api/v1/carreras?q=Sistemas&area=Salud").json()["total"] == 0


def test_search_does_not_interpret_wildcards(client):
    assert client.get("/api/v1/carreras?q=%25").json()["total"] == 0


def test_unknown_district_not_inferred(client):
    offers = client.get("/api/v1/ofertas?career_id=0").json()["items"]
    assert all(offer["district"] is None for offer in offers)
    assert client.get("/api/v1/catalogo/filtros").json()["districts"] == []


def test_cost_and_provenance_preserved(client):
    c01 = client.get("/api/v1/ofertas/C01").json()
    assert c01["cost"] == "775.00" and c01["cost_status"] == "estimado"
    c05 = client.get("/api/v1/ofertas/C05").json()
    assert c05["cost"] == "0.00" and "primera carrera" in c05["detail"]["estado_costo"]


def test_comparison_has_twelve_criteria(client):
    result = client.post("/api/v1/comparaciones/preview", json={"career_ids": [0, 1]})
    assert result.status_code == 200
    assert len(result.json()["criteria"]) == 12
    assert result.json()["careers"][0]["name"] == "Ingeniería de Sistemas"


def test_duplicate_missing_and_boolean_career_rejected(client):
    for ids, code in [([0, 0], 422), ([0, 999], 404), ([False, 1], 422)]:
        assert (
            client.post("/api/v1/comparaciones/preview", json={"career_ids": ids}).status_code
            == code
        )


def test_cost_range_has_no_single_monthly_amount(seeded, records, editorial):
    modified = copy.deepcopy(records)
    modified[0].update(costo_mensual_soles=None, costo_minimo=650, costo_maximo=1200)
    with seeded[1].begin() as session:
        import_catalog(SqlCatalogImporter(session), modified, editorial)
        offer = session.get(Offer, "C01")
        assert offer.cost is None and float(offer.cost_min) == 650 and float(offer.cost_max) == 1200


def test_import_changes_catalog_version_when_cost_changes(seeded, records, editorial):
    with seeded[1]() as session:
        old_version = session.get(Career, 0).version
    modified = copy.deepcopy(records)
    modified[0]["costo_mensual_soles"] = 800
    with seeded[1].begin() as session:
        import_catalog(SqlCatalogImporter(session), modified, editorial)
        assert session.get(Career, 0).version != old_version
