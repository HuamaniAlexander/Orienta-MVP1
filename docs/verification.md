# Verificación de entrega · 25/10/2026

Código funcional validado: commit remoto `8d5fa16ae8377bab1a9e617a810537303df8c3f8` (17 commits de implementación).

| Verificación | Resultado y alcance |
|---|---|
| Ruff | Check y formato correctos en backend, ML, paquete compartido y scripts |
| Pytest local | 28 aprobadas; SQLite aislado, FK activas |
| Pytest CI | Aprobado con PostgreSQL 17 real; cada caso usa esquema separado |
| Migración Alembic CI | upgrade head aprobado sobre PostgreSQL; importador ejecutado correctamente |
| Frontend | 3 pruebas aprobadas y compilación TypeScript/Vite correcta |
| Playwright local | Flujo completo de escritorio y búsqueda/vacío móvil aprobados; un proceso Chromium por escenario por restricciones del entorno |
| Playwright CI | Paso completo aprobado con navegador estándar del runner |
| Datos en InsForge | Esquema orienta con 11 carreras, 19 ofertas y 18 diccionarios comprobados mediante SQL administrativo |
| Secretos | 95 archivos rastreados revisados; clave de usuario y .env excluidos |
| Revisión visual | Catálogo y comparación inspeccionados en navegador a 1600px; filtros y columnas alineados |

Evidencia CI: https://github.com/HuamaniAlexander/Orienta-MVP1/actions/runs/40170338958

La última corrección documental ajusta el setup de Colab para exportar dependencias del lockfile en vez de intentar instalar el monorepo virtual con pip. No afirma ejecución de un entrenamiento sin datos.

## Estado de datos y alcance

El acceso administrativo HTTPS permitió crear/verificar las tablas. La conexión PostgreSQL directa no resuelve por DNS desde el entorno de edición; queda configurada de forma privada para un alojamiento con acceso de red. Esto no se presenta como una prueba end-to-end contra el host InsForge. La integración ORM se comprobó con PostgreSQL real en CI.

No se entrenó un recomendador supervisado porque no existen respuestas/etiquetas reales. El módulo de entrenamiento, validación agrupada, exportación e inferencia está implementado, con artefactos experimentales bloqueados en producción. Gemini no se probó con una clave real: se comprobó su contingencia con un timeout simulado.

El catálogo recibido tiene costos estimados y no identifica distritos exactos. No se fabricaron tarifas, mallas estructuradas, distritos ni ofertas técnicas. La aplicación permite completar/revisar esos datos, preserva su procedencia y no promete orientación validada sin revisión académica.

No se desplegó un sitio externo, no se fusionó main y no se registraron tarjetas en Trello. El PR se mantiene como borrador para revisión.
