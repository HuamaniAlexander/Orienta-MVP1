import hashlib
import json
from decimal import Decimal

from app.adapters.outbound.persistence.models import Career, ImportBatch, Institution, LegacyCode, Offer
from app.domain.errors import DomainError


def validate_rows(rows):
    if not rows:
        raise DomainError("El catálogo está vacío")
    maps, ids, codes = {}, set(), set()
    required = {"id_carrera", "id_carrera_codigo", "carrera", "institucion",
                "institucion_codigo", "grupo_carrera", "grupo_carrera_codigo",
                "area_formacion", "area_formacion_codigo", "duracion_meses", "modalidad",
                "modalidad_codigo", "ubicacion", "costo_mensual_soles", "estado_costo",
                "fecha_revision", "fuente_carrera"}
    for index, row in enumerate(rows, 2):
        if not required.issubset(row):
            raise DomainError(f"Fila {index}: faltan columnas obligatorias")
        if row["id_carrera"] in ids or row["id_carrera_codigo"] in codes:
            raise DomainError(f"Fila {index}: identificador duplicado")
        ids.add(row["id_carrera"]); codes.add(row["id_carrera_codigo"])
        if not isinstance(row["duracion_meses"], (int, float)) or row["duracion_meses"] <= 0:
            raise DomainError(f"Fila {index}: duración inválida")
        cost = row["costo_mensual_soles"]
        if cost is not None and (not isinstance(cost, (int, float)) or cost < 0):
            raise DomainError(f"Fila {index}: costo inválido")
        for key, code in row.items():
            if not key.endswith("_codigo"):
                continue
            field = key.removesuffix("_codigo")
            if type(code) is not int or field not in row or row[field] is None:
                raise DomainError(f"Fila {index}: código inválido en {key}")
            value = str(row[field])
            mapping = maps.setdefault(field, {})
            if (code in mapping and mapping[code] != value) or any(
                    k != code and v == value for k, v in mapping.items()):
                raise DomainError(f"Fila {index}: equivalencia inconsistente en {field}")
            mapping[code] = value
    return maps


def import_catalog(session, rows, editorial, dry_run=False):
    maps = validate_rows(rows)
    digest = hashlib.sha256(json.dumps([rows, editorial], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    # Validar tanto código->texto como texto->código contra el registro histórico.
    from sqlalchemy import select
    for old in session.scalars(select(LegacyCode)):
        current = maps.get(old.field, {})
        if old.code in current and current[old.code] != old.value:
            raise DomainError(f"No se permite reasignar el código {old.field}:{old.code}")
        if any(k != old.code and v == old.value for k, v in current.items()):
            raise DomainError(f"No se permite recodificar {old.field}")
    counts = {"offers": len(rows), "careers": len({r['grupo_carrera_codigo'] for r in rows}),
              "dictionaries": len(maps), "unchanged": bool(session.get(ImportBatch, digest))}
    if dry_run or counts["unchanged"]:
        return counts
    for field, mapping in maps.items():
        for code, value in mapping.items():
            if not session.get(LegacyCode, (field, code)):
                session.add(LegacyCode(field=field, code=code, value=value))
    for row in rows:
        institution = session.get(Institution, row["institucion_codigo"])
        if not institution:
            institution = Institution(code=row["institucion_codigo"], name=row["institucion"], kind="universidad")
            session.add(institution)
        code = row["grupo_carrera_codigo"]
        career = session.get(Career, code)
        if not career:
            ed = editorial.get(row["grupo_carrera"], {})
            career = Career(code=code, slug=row["grupo_carrera"], name=ed.get("name",row["carrera"]),
                            area=row["area_formacion"], area_code=row["area_formacion_codigo"],
                            kind="universitaria", content=ed, profile=ed.get("demo_profile"),
                            profile_reviewed=False, version=digest[:12])
            session.add(career)
        # No inferir distrito a partir de Campus Lima Norte ni de Lima.
        offer = session.get(Offer, row["id_carrera"])
        values = dict(legacy_code=row["id_carrera_codigo"], career_code=code,
                      institution_code=row["institucion_codigo"], modality=row["modalidad"],
                      modality_code=row["modalidad_codigo"], district=row.get("distrito"),
                      location_legacy=row["ubicacion"], months=int(row["duracion_meses"]),
                      cost=Decimal(str(row["costo_mensual_soles"])) if row["costo_mensual_soles"] is not None else None,
                      cost_status="estimado" if "estimad" in row["estado_costo"].lower() else "verificado",
                      detail=row, active=True)
        if not offer:
            session.add(Offer(id=row["id_carrera"], **values))
        else:
            for key, value in values.items():
                setattr(offer, key, value)
        session.flush()
    session.add(ImportBatch(digest=digest, counts=counts))
    session.flush()
    return counts
