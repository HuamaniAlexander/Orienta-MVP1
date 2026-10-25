# Artefactos
El entrenamiento genera pipeline.joblib, manifest.json, metrics.json y model_card.md. Los modelos comienzan en estado experimental. No hay métricas prefijadas ni artefacto entrenado con datos ficticios.

Para promover: revisión experta de datos, comparación con referencias, particiones independientes, intervalos por participante y análisis de errores. El responsable documenta su decisión y actualiza status=approved solo si se cumplen los criterios. El adaptador valida hash, versión sklearn y orden de features. Cargar únicamente artefactos propios y confiables.
