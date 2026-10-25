# ORIENTA · MVP 1

Aplicación académica para comparar **dos carreras** y explorar después la misma carrera por institución y sede. React + TypeScript, FastAPI, arquitectura hexagonal y PostgreSQL. InsForge se utiliza exclusivamente como alojamiento PostgreSQL; no se usan su Auth, funciones ni servicios IA.

## Funcionalidades

- Nueve páginas: Inicio, Catálogo, Ficha, Comparación, Cuestionario, Resultado, Login, Registro y Mi cuenta (perfil + historial).
- Búsqueda y filtros combinados; selección de dos carreras; comparación de 12 criterios.
- Instituciones y sedes como segundo paso opcional; enlaces al plan oficial para comparar mallas.
- Cuestionario de ocho preguntas de interés y cuatro pasos de condiciones. Afinidad explicable separada de presupuesto/distrito.
- Sesiones propias, Argon2id, cookie HttpOnly, CSRF, acceso por propietario, snapshots e idempotencia.
- Importación JSON/Excel con 18 diccionarios preservados, dry-run y rollback.
- Código y notebooks Colab para entrenamiento real futuro; Gemini opcional y restringido, con plantilla local.

## Instalación

Requisitos: Python 3.12+, uv, Node 22+ y PostgreSQL 17+ (o cadena PostgreSQL InsForge). Desde la raíz:

```bash
uv sync --all-extras
npm --prefix frontend ci
cp .env.example .env
```

Completar DATABASE_URL **en .env local**, nunca en Git ni en variables VITE_. Usar la cadena de conexión real del panel InsForge, no una API key como contraseña PostgreSQL. El runtime no necesita la clave administrativa InsForge.

```bash
# Opcional para PostgreSQL local:
docker compose up -d postgres
# Migrar e importar, siempre desde la raíz:
PYTHONPATH=backend uv run alembic -c backend/alembic.ini upgrade head
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.import_catalog data/catalogo_legacy.json --dry-run
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.import_catalog data/catalogo_legacy.json
# API en terminal 1:
PYTHONPATH=backend uv run uvicorn main:app --reload
# Frontend en terminal 2 (proxy /api a FastAPI):
npm --prefix frontend run dev
```

Windows PowerShell: definir `$env:PYTHONPATH="backend"` y ejecutar los mismos comandos sin el prefijo `PYTHONPATH=backend`. Frontend: http://localhost:5173; OpenAPI: http://localhost:8000/docs.

## Demo local explícita

Para revisar interfaces y flujo sin conectarse a la base externa:

```bash
npm --prefix frontend run build
PYTHONPATH=backend uv run uvicorn scripts.demo:make_app --factory --host 127.0.0.1 --port 8000
```

Abrir http://127.0.0.1:8000. Este modo usa SQLite aislado en demo.db y perfiles editoriales **ilustrativos**, etiquetados como tales. No es el despliegue productivo. La configuración de producción rechaza DEMO_MODE=true.

## Datos reales y límites actuales

El archivo original aporta 19 ofertas de UTP/UNMSM, 13 nombres y 11 grupos normalizados. Se conservan C01–C19 y sus códigos 0–18. El catálogo incluido no contiene ofertas técnicas; no se agregaron institutos ficticios para llenar filtros.

Los 13 importes UTP de S/775 son estimaciones declaradas por el archivo. S/0 en UNMSM describe enseñanza de primera carrera y no costo total cero. El diseño admite montos/rangos con su alcance. No se presentan estimaciones como tarifas oficiales.

No hay distritos específicos en el archivo: Campus Lima Norte y Lima se conservan solo como procedencia, **no** se inventa un distrito. Para publicar una sede por distrito se debe completar la columna `distrito` en una importación revisada. La UI principal no usa Campus Lima Norte.

Las descripciones de carrera son síntesis editoriales generales, no la malla particular de una universidad. Los enlaces de cada institución permiten revisar el plan oficial. Todavía se necesita completar mallas estructuradas, distritos, costos actuales y ofertas técnicas con fuentes institucionales.

Los perfiles incluidos son borradores, no un instrumento validado. Fuera de demo, no se publica una puntuación sin revisión. Para aprobar perfiles reales:

```bash
PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.review_profiles perfiles_revisados.json
```

Formato privado: lista de objetos `{career_id, profile:[seis números 0–1], reviewers:[dos nombres diferentes], sources:[URLs], rubric_version, reviewed_at:"AAAA-MM-DD"}`. Requiere revisión humana efectiva, no solo llenar el JSON.

## IA y Colab

`ml/notebooks/` documenta auditoría y entrenamiento offline. El entrenamiento utiliza perfiles y etiquetas reales independientes, separados por participante. Entrena logística, árbol y bosque, comparados con Dummy y baseline de contenido. No genera etiquetas desde las reglas, ni métricas prefijadas.

```bash
uv run python -m ml.src.train afinidad_etiquetada.csv metadata.json --output ml/artifacts/experiment
```

El catálogo de carreras **no es un dataset supervisado de afinidad**. No se entrega un modelo entrenado ficticio ni se promete >90 %. Los artefactos empiezan como experimentales; solo después de revisión independiente pueden aprobarse y configurarse con MODEL_PATH. FastAPI carga el artefacto una vez por proceso; no necesita Colab abierto.

Gemini se habilita únicamente con GEMINI_API_KEY y GEMINI_MODEL en backend. Por seguridad, solo ordena razones de un banco permitido: no modifica puntuaciones ni inventa costos, mallas o salarios. Ante error/cuota/timeout, se usa plantilla.

## Validación

```bash
uv run ruff check backend ml packages scripts
uv run ruff format --check backend ml packages scripts
uv run pytest -q
npm --prefix frontend test
npm --prefix frontend run build
# PostgreSQL real de pruebas, nunca la base compartida de producción:
TEST_DATABASE_URL=postgresql+psycopg://orienta:orienta@localhost:5432/orienta uv run pytest -q
# Con demo ya iniciada y Chromium instalado:
cd frontend
npx playwright install chromium
npm run test:e2e
```

Sin TEST_DATABASE_URL se ejecutan pruebas rápidas SQLite con FK activas. Con esa variable, cada prueba crea y elimina un esquema PostgreSQL único. CI usa PostgreSQL real como servicio y ejecuta también el flujo de navegador.

## Publicación

Ver docs/deployment.md. `npm --prefix frontend run build` permite servir React desde FastAPI bajo el mismo origen. El Dockerfile empaqueta la aplicación, nunca .env ni datasets personales. Configurar DATABASE_URL y COOKIE_SECURE=true en el alojamiento. No se desplegó un servicio web externo como parte de este repositorio.

## Trabajo en equipo

main permanece estable; dev integra; feature/* agrupa módulos; release/0.1.0 prepara revisión; hotfix/* corrige versiones publicadas. Commits atómicos en español. Ver docs/gitflow.md, docs/backlog.md y docs/testing.md. No hay scripts que publiquen secretos ni que modifiquen ramas protegidas automáticamente.
