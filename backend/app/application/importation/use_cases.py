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



def import_catalog(importer, rows, editorial, dry_run=False):
    validate_rows(rows)
    return importer.import_rows(rows, editorial, dry_run)
