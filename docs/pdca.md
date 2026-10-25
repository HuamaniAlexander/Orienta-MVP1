# PDCA y trazabilidad

| Fase | Caso | Evidencia |
|---|---|---|
| Plan | HU04: comparar dos carreras y rechazar la misma dos veces | Contrato PairIn y criterio de 12 filas |
| Do | Implementación de check_pair y preview | Dominio y caso de uso, commits de catálogo/API |
| Check | test_comparison_has_twelve_criteria y test_duplicate_missing_and_boolean_career_rejected | Ejecución Pytest local y CI |
| Act | Mantener restricciones y regresión en el flujo | Pruebas recurrentes y revisión de contrato |

Defecto detectado durante validación: un TestClient secundario cerraba un engine inyectado compartido; se corrigió para disponer solo conexiones creadas por la propia aplicación. Se repitieron las pruebas de historial/usuario A-B y pasaron.

Otro ajuste: la paginación borraba page incluso al cambiar de página. Se conserva al paginar y solo se reinicia al modificar filtros. No se inventan encuestas de usabilidad ni resultados de eficacia vocacional.
