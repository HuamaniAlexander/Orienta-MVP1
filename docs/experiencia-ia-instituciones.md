# Nota de actualización

Esta página conserva la descripción de la entrega anterior. El estado vigente está en [Catálogo completado](catalogo-completado.md), [Recomendador por contenido](recomendador-contenido.md) y [Verificación](verification.md): 37 instituciones, 24 programas con tarifas y modelo de contenido entrenado.

# Mejora de experiencia, instituciones e IA

## Producto

El inicio y el directorio incorporan dos ilustraciones originales de ORIENTA, con colores azul marino, turquesa, menta y crema. Las tarjetas conservan columnas simétricas y se adaptan a una, dos o tres columnas. El directorio tiene búsqueda sin distinción de acentos, filtro por distrito y tipo de institución, limpieza de filtros, contador y estados de carga/error/vacío. Las ubicaciones muestran distritos, sin usar «Campus Lima Norte» como etiqueta de sede.

Las fichas del directorio son entidades geográficas independientes de las ofertas: que una institución aparezca no significa que dicte todas las carreras del catálogo. Los programas visibles proceden de las fuentes de cada ficha, y las tarifas deben conservar modalidad, periodo y alcance.

## Datos y operación

Se incorporan 17 instituciones y se revisan diez cuotas de UTP para ingresantes por examen en agosto de 2026. Las guías publican cuotas base, no el costo total de una carrera. La revisión no se aplica a modalidades ni programas fuera del alcance de la fuente. El archivo legado permanece intacto.

```bash
PYTHONPATH=backend uv run alembic -c backend/alembic.ini upgrade head
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.import_catalog data/catalogo_legacy.json
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.import_directory
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.review_offers data/revisiones_ofertas.json
```

La revisión de ofertas invalida la versión de comparación, es idempotente y no aprueba perfiles vocacionales. InsForge se utiliza únicamente para PostgreSQL. El directorio se sirve desde la base, sin descargar sitios externos en cada visita.

Fuentes principales:

- [Directorio DRELM de institutos públicos](https://www.drelm.gob.pe/drelm/wp-content/uploads/2024/02/PDF-Directorio-de-institutos-publicos-de-Lima-Metropolitana.pdf), edición 2024. No se presenta como garantía de convocatoria abierta actual.
- [Guías oficiales UTP de agosto de 2026](https://admision.zendesk.com/hc/es/articles/4408793359757-Gu%C3%ADas-del-Ingresante-Agosto-2026).
- [Presencial, guía ADM–GU1311](https://admision.zendesk.com/hc/article_attachments/44776567153805).
- [Semipresencial y distancia 80/20, guía ADM–GU1326](https://admision.zendesk.com/hc/article_attachments/44776895525517).
- Las demás fuentes se incluyen por institución en `data/instituciones_lima_norte.json`.

## Recomendación y explicación

Gemini recibe exclusivamente respuestas de preguntas cerradas, preferencias y hechos de las dos carreras. No recibe correo, contraseña, sesión ni historial. Su salida JSON contiene un resumen, explicación individual y siguiente paso. Se validan los identificadores, longitud, tipo y ausencia de cifras, enlaces o HTML. El texto se renderiza como texto React. Estas validaciones reducen riesgos; no equivalen a verificar semánticamente cada afirmación de un modelo generativo.

La explicación generativa no modifica puntuaciones. El motor de afinidad exige perfiles revisados en producción; el módulo supervisado exige un artefacto aprobado. Sin esas condiciones se ofrece exploración cualitativa, sin inventar porcentajes ni afirmar que existe un modelo entrenado. Ante error o espera de Gemini se utiliza la explicación local, identificada internamente con `mode=template`.

Configurar `GEMINI_API_KEY` y `GEMINI_MODEL` solo en el servidor. El ejemplo utiliza `gemini-3.8-flash`, disponible según [documentación oficial](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash). Los tests aíslan la configuración y simulan respuestas para no consumir una clave local accidentalmente.

## Alcance pendiente verificable

Esta entrega no es un censo exhaustivo de todas las instituciones de los ocho distritos de Lima Norte. Tampoco agrega todas sus ofertas, mallas desglosadas, requisitos particulares, becas ni tarifarios vigentes. Esos datos requieren fuentes de cada institución y convocatoria. Las estimaciones antiguas no se muestran como importes publicados ni se usan en el rango financiero de comparación.

No existe aún un dataset real con etiquetas académicas suficiente para entrenar y validar un recomendador supervisado. El contenido editorial de perfiles se mantiene sin aprobación hasta revisión especializada. No se habilita modo demostrativo en producción para simular esa validación.
