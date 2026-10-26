# Verificación · 25/10/2026

| Comprobación | Resultado |
|---|---|
| Backend local | 42 pruebas aprobadas, Ruff y formato |
| Frontend | 3 pruebas y compilación TypeScript/Vite |
| Navegador | 9 escenarios aprobados: seis anchuras 320–1920 px, comparación/cuenta/historial, búsqueda móvil y programas/precios/opciones técnicas |
| Entrenamiento | TF-IDF ajustado sobre 13 documentos; 398 características; artefacto JSON y manifest con hashes |
| Paridad | Inferencia Python comparada numéricamente con scikit-learn |
| Gemini real | API completa respondió HTTP 200, `content_based`, `gemini_grounded`, dos narrativas y `demo=false` |
| Padrón | 17 de 17 institutos del snapshot MINEDU cubiertos; 37 instituciones en directorio |
| Datos | 24 fichas de programas con tarifa o rango, periodo, alcance y fuente |
| Auditoría | Se conservan los 19 registros legado; ocho ofertas y una carrera salen de publicación por falta de alcance documentado |
| InsForge | Migración 0003, 37 instituciones, 24 programas y 13 carreras almacenadas; auditoría de alcance aplicada |

La ejecución de Gemini utilizó la clave privada solo en servidor y entradas de prueba de software. No se creó un alumno ni una cuenta en la base compartida. La prueba de API utilizó SQLite aislado; la comprobación de InsForge fue por SQL administrativo, no se presenta como prueba de la conexión ORM directa desde este entorno.

Las pruebas incluyen hashes, desconocidos, presupuestos por intervalo, idempotencia, aislamiento de historial, versionado y bloqueo de textos generativos con cifras no permitidas. El árbol de código se comprueba al publicar. Las pruebas con PostgreSQL real y navegador estándar se ejecutan en GitHub Actions.

No se atribuye validez psicométrica al índice temático, ni se entrenó una predicción supervisada con etiquetas inexistentes. El notebook supervisado permanece como alternativa independiente. El [informe de cobertura](data-coverage.json) distingue instituciones registradas de programas y precios efectivamente cargados; no certifica un censo de todas las filiales y convocatorias de Lima Norte.
