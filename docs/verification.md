# Verificación de entrega · 25/10/2026

| Verificación | Resultado y alcance |
|---|---|
| Ruff | Check y formato del backend, ML, paquete compartido y scripts |
| Pytest local | 34 aprobadas; SQLite aislado, FK activas |
| Frontend | 3 pruebas aprobadas y compilación TypeScript/Vite |
| Playwright local | 8 escenarios aprobados: flujo de comparación/cuenta/historial, búsqueda móvil y seis tamaños de pantalla |
| Responsive | Inicio, directorio, catálogo, detalle, comparación, cuestionario y estados iniciales de resultado/cuenta/autenticación comprobados a 320, 390, 768, 1024, 1440 y 1920 px |
| Recursos | Imágenes cargadas realmente en navegador; WebP 640/1280; revisión visual de inicio móvil y directorio escritorio |
| InsForge | 17 fichas de instituciones y 10 revisiones de cuotas verificadas por SQL; se conservan 11 carreras y 19 ofertas originales |
| Secretos | Claves y `.env` fuera de archivos publicados; Gemini solo en backend |
| Gemini real | Consulta de modelos autenticada; generación devolvió alta demanda HTTP 503 o timeout, por lo que se comprobó la contingencia local |
| Gemini simulado | Respuesta personalizada por carrera aceptada; cifras inventadas rechazadas; afinidad conservada |

La revisión responsive detectó y corrigió un desbordamiento del cuestionario a 320 px y una jerarquía de títulos oculta en móvil. La navegación frecuente ya no consume el límite reservado a intentos de autenticación; los POST de acceso mantienen el límite y su prueba.

La CI de la entrega anterior aprobó PostgreSQL real, migración y Playwright estándar: https://github.com/HuamaniAlexander/Orienta-MVP1/actions/runs/40170594749 . La nueva revisión debe ejecutar esa misma CI con migración `0002`, importación del directorio y revisión de cuotas.

## Límites comprobados

La conexión PostgreSQL directa no resuelve por DNS desde el entorno de edición. El canal administrativo HTTPS se utilizó para provisionar/verificar, sin incorporarlo al runtime. Esto no es una prueba end-to-end de la aplicación contra InsForge.

No hay dataset real etiquetado ni artefacto supervisado entrenado/aprobado. No se generaron etiquetas ni métricas ficticias. La recomendación generativa no se considera validada en vivo mientras el proveedor no complete una respuesta satisfactoria.

El directorio no es exhaustivo ni sustituye la oferta detallada de cada institución. Las diez cuotas revisadas tienen alcance de agosto de 2026; no se extrapolan a otros periodos. No se fabricaron mallas ni tarifas para rellenar campos. Véase [fuentes y alcance](experiencia-ia-instituciones.md).

No se ha desplegado un sitio externo ni fusionado `main`.
