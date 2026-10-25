# Datos de entrenamiento
No existe un dataset supervisado adjunto. El catálogo no permite entrenar recomendaciones personales.

CSV privado: participant_id, las seis columnas sim_* de orienta_features.FEATURES y y (0/1). Una fila por participante–carrera evaluada. Mantener IDs de carrera y versiones en el archivo privado de trazabilidad, fuera de las features. Los revisores no ven predicciones. Los casos indeterminados no se fuerzan a y. Nunca usar la fórmula como etiqueta.

Metadatos JSON: label_source="expert_review", consent_documented=true, profiles_reviewed=true, dataset_version, rubric_version y reviewers. Estos indicadores documentan una revisión humana; no la reemplazan.

El paquete orienta_features construye las features en Colab y FastAPI. Recolección y revisión deben preceder al entrenamiento. No subir datos de participantes a este repositorio público. Los CSV están ignorados por Git.
