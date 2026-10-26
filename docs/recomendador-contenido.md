# Recomendador aprendido de contenido académico

El MVP utiliza un modelo TF-IDF ajustado con scikit-learn sobre trece documentos académicos breves: once grupos del catálogo original y dos programas técnicos distintos de los universitarios. Son síntesis trazables de programas reales. Se aprenden el vocabulario y la frecuencia inversa de sus términos; no se crean alumnos, etiquetas ni porcentajes de éxito ficticios.

Las ocho respuestas cerradas construyen una consulta ponderada de temas. El vocabulario de cada pregunta es una decisión explícita de diseño, no un parámetro aprendido de alumnos. Las respuestas nulas se omiten; se requieren al menos cuatro conocidas y algún interés positivo. La similitud coseno compara esa consulta con cada carrera. Se muestran coincidencias de términos y sus fuentes. Una diferencia menor a tres puntos se presenta como cercana; es una regla de interfaz y no un umbral psicométrico validado.

## Entrenar y entregar

```bash
uv sync --frozen --extra ml
uv run --extra ml python -m ml.src.train_content
```

También puede ejecutarse `ml/notebooks/03_recomendador_contenido.ipynb` en Colab. Exporta `data/models/contenido.json` y su manifest, con hashes del corpus y artefacto. FastAPI carga el JSON al iniciar y calcula la inferencia con Python estándar: no necesita instalar scikit-learn en producción, ejecutar entrenamientos durante una petición ni mantener Colab abierto. El runtime se prueba contra las transformaciones de scikit-learn para evitar diferencias entre entrenamiento e inferencia.

El corpus completo tiene trece documentos; el catálogo público publica doce carreras con programas institucionales documentados. El programa independiente de Psicología Organizacional del legado queda conservado y retirado de publicación al no tener oferta documentada en las instituciones objetivo. Su documento permanece como contexto del corpus, sin presentarse como una opción disponible.

## Gemini y presupuesto

`GEMINI_MODEL=gemini-3.5-flash-lite` es el modelo que completó las pruebas reales. Recibe respuestas, coincidencias y condiciones publicadas; devuelve resumen, explicación por carrera y siguiente paso. No cambia puntuaciones, ni decide la escala económica de un estudiante. Sin Gemini disponible, el modelo de contenido sigue funcionando y conserva razones locales verificables.

Un presupuesto inferior al mínimo de una escala se identifica como fuera de rango; si alcanza el máximo está dentro de la cuota publicada; entre ambos extremos depende de la escala asignada. No se utiliza el punto medio como precio personal. Matrícula y otros conceptos siguen separados. El presupuesto no cambia el interés académico calculado.

## Validación y límites

Las pruebas verifican paridad numérica con scikit-learn, cambios ante distintos intereses, rechazo de un artefacto alterado y manejo de desconocidos. La prueba real de API completó `mode=content_based`, `explanation.mode=gemini_grounded`, dos narrativas y `demo=false`.

No se atribuyen accuracy ni F1 a un modelo sin etiquetas de pertinencia reales. El entrenamiento supervisado sigue siendo una línea independiente y opcional, no una dependencia para que este recomendador funcione. La calidad del corpus y del vocabulario de preguntas requiere evaluación continua con usuarios; coincidencia temática no equivale a aptitud o éxito académico.
