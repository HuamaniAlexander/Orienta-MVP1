import hashlib
import json
from decimal import Decimal

from app.application.importation.use_cases import validate_rows
from app.domain.errors import DomainError

from .models import Career, ImportBatch, Institution, LegacyCode, Offer


def import_catalog_sql(session, rows, editorial, dry_run=False):
    maps = validate_rows(rows)
    digest = hashlib.sha256(
        json.dumps([rows, editorial], sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    # Validar tanto código->texto como texto->código contra el registro histórico.
    from sqlalchemy import select

    for old in session.scalars(select(LegacyCode)):
        current = maps.get(old.field, {})
        if old.code in current and current[old.code] != old.value:
            raise DomainError(f"No se permite reasignar el código {old.field}:{old.code}")
        if any(k != old.code and v == old.value for k, v in current.items()):
            raise DomainError(f"No se permite recodificar {old.field}")
    counts = {
        "offers": len(rows),
        "careers": len({r["grupo_carrera_codigo"] for r in rows}),
        "dictionaries": len(maps),
        "unchanged": bool(session.get(ImportBatch, digest)),
    }
    if dry_run or counts["unchanged"]:
        return counts
    for field, mapping in maps.items():
        for code, value in mapping.items():
            if not session.get(LegacyCode, (field, code)):
                session.add(LegacyCode(field=field, code=code, value=value))
    for row in rows:
        institution = session.get(Institution, row["institucion_codigo"])
        if not institution:
            institution = Institution(
                code=row["institucion_codigo"], name=row["institucion"], kind="universidad"
            )
            session.add(institution)
        code = row["grupo_carrera_codigo"]
        career = session.get(Career, code)
        if not career:
            ed = editorial.get(row["grupo_carrera"], {})
            career = Career(
                code=code,
                slug=row["grupo_carrera"],
                name=ed.get("name", row["carrera"]),
                area=row["area_formacion"],
                area_code=row["area_formacion_codigo"],
                kind="universitaria",
                content=ed,
                profile=ed.get("demo_profile"),
                profile_reviewed=False,
                version=digest[:12],
            )
            session.add(career)
        # No inferir distrito a partir de Campus Lima Norte ni de Lima.
        offer = session.get(Offer, row["id_carrera"])
        values = dict(
            legacy_code=row["id_carrera_codigo"],
            career_code=code,
            institution_code=row["institucion_codigo"],
            modality=row["modalidad"],
            modality_code=row["modalidad_codigo"],
            district=row.get("distrito"),
            location_legacy=row["ubicacion"],
            months=int(row["duracion_meses"]),
            cost=Decimal(str(row["costo_mensual_soles"]))
            if row["costo_mensual_soles"] is not None
            else None,
            cost_status="estimado" if "estimad" in row["estado_costo"].lower() else "verificado",
            detail=row,
            active=True,
        )
        if not offer:
            session.add(Offer(id=row["id_carrera"], **values))
        else:
            for key, value in values.items():
                setattr(offer, key, value)
        session.flush()
    session.add(ImportBatch(digest=digest, counts=counts))
    session.flush()
    return counts


class SqlCatalogImporter:
    def __init__(self, session):
        self.session = session

    def import_rows(self, rows, editorial, dry_run=False):
        return import_catalog_sql(self.session, rows, editorial, dry_run)
