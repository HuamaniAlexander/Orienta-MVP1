# Catálogo institucional: cobertura y procedencia

La actualización incorpora 37 instituciones, 24 fichas de programas y tarifas publicadas en las 24 fichas, con cuota o rango, periodo, alcance y fuente. Se documentan dos programas técnicos de tres años, sin confundir Enfermería Técnica con Enfermería universitaria ni Gestión Administrativa con Administración universitaria.

## Cobertura comprobable

El padrón MINEDU actualizado al 23 de junio de 2026 contiene diecisiete institutos con sede principal registrada en los distritos seleccionados; los diecisiete están representados. El JSON conserva código modular, fecha y hash del XLSX descargado. El directorio también incluye universidades, sedes y otras instituciones verificadas en sus portales. El ámbito principal comprende los ocho distritos habituales de Lima Norte; se conserva Rímac como ámbito cercano para UNI y el instituto de las Fuerzas Armadas.

Esta cobertura del padrón no demuestra que se hayan censado todas las filiales, pedagógicos, centros militares y programas existentes. Tampoco convierte un rango institucional general, como el de UPN, en tarifa de cada carrera. `docs/data-coverage.json` informa explícitamente cuántos programas y precios están cargados por institución. No todas las 37 fichas tienen todavía programas con tarifas individuales.

## Fuentes destacadas

- [MINEDU · padrón oficial XLSX](https://cdn.www.gob.pe/uploads/document/file/5244774/4718331-4718331-listado-de-institutos-de-educacion-superior-licenciados%282%29.xlsx?v=1782926377).
- [UCH · resolución de costos 2026](https://www.uch.edu.pe/cdn/pdf/001-2026_APRUEBA_COSTOS_2026_1_res.pdf) y [planes, admisión y becas](https://www.uch.edu.pe/conocenos/transparencia).
- [Cayetano · rangos por carrera 2026](https://blogs.cayetano.edu.pe/pregrado/cayetano-heredia-mensualidad/), sujetos a evaluación socioeconómica.
- [André Vesalio · tasas económicas 2026](https://www.institutovesalio.edu.pe/documents/transparencia/tasas-economicas.pdf).
- [UPN · política de pensiones](https://www.upn.edu.pe/transparencia/pensiones-tarifas); el rango es institucional y varía por carrera, sede y modalidad.
- Los planes UTP se enlazan desde cada programa y se conservan sus periodos de tarifa. Arquitectura utiliza la guía de marzo de 2026 y se identifica como tal.

Las síntesis del corpus no sustituyen la malla particular. La comparación secundaria muestra la denominación oficial de cada programa y permite abrir su documentación; no atribuye a una sede el plan de otra institución. Los documentos financieros que no especifican una sede se identifican a nivel institucional.

## Auditoría y cargas

Ocho ofertas antiguas se conservan en la base pero salen de publicación: seis no documentan un distrito objetivo y dos usan un rótulo de virtualidad sin porcentaje presencial o tarifa aplicable. Una carrera independiente sin programa documentado en las instituciones objetivo se conserva fuera del catálogo público. El archivo legado no se altera.

```bash
PYTHONPATH=backend uv run alembic -c backend/alembic.ini upgrade head
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.import_catalog data/catalogo_legacy.json
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.import_directory
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.review_offers data/revisiones_ofertas.json
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.import_programs
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.audit_offers
uv run python scripts/data_coverage.py
```

Las nuevas cargas operan en transacciones, conservan las identidades del legado y permiten repetirlas. La versión de detalle deriva de los datos y programas publicados; el par de comparación usa un hash de longitud fija. Una revisión de precio, programa o alcance invalida comparaciones desactualizadas sin modificar el historial ya guardado.
