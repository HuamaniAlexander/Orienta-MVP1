# Despliegue y operación

1. Completar DATABASE_URL con TLS desde el panel de InsForge. No utilizar la clave administrativa en el cliente. Configurar un rol con permisos solo sobre orienta si el proveedor lo permite.
2. Aplicar Alembic en una tarea de administración, no en cada arranque. Importar catálogo en transacción única. Respaldar antes de migraciones de cambios reales.
3. Construir Dockerfile o instalar con uv y compilar frontend. Servir FastAPI detrás de HTTPS bajo un origen.
4. Configurar APP_ENV=production, COOKIE_SECURE=true, DEMO_MODE=false y ALLOWED_ORIGINS con el dominio exacto. No publicar .env.
5. Verificar /api/v1/health/live y /api/v1/health/ready. La segunda requiere catálogo y conexión DB. Gemini no condiciona readiness.
6. Inicialmente un proceso worker; el rate limiter es en memoria por proceso. Antes de escalar, centralizar límites en el proxy o un almacén compartido. Configurar límite de body de 16 KiB en el proxy; la API valida tipos/longitudes y Content-Length, pero no se presenta como límite total de tráfico chunked.
7. Programar purga de browser_session expiradas mediante SQL restringido a orienta. No imprimir cookies, contraseñas, respuestas o cadenas DB en logs.
8. Mantener copia del artefacto anterior aprobado y su manifest para rollback. No subir archivos joblib arbitrarios desde HTTP.

No se incluye un servicio de correo ni recuperación de contraseña. El piloto requiere soporte del responsable antes de apertura masiva de cuentas. Definir retención, atención de eliminación de cuentas y consentimiento institucional para investigaciones con menores antes de recolectar datos reales.

La conexión directa del entorno de desarrollo remoto puede depender de DNS/red. La API administrativa solo se utilizó para provisionar/verificar la base; **no es el canal de consultas del runtime**. No existe dependencia de una sesión MCP o de Colab.

Comprobar restauración de una copia en base aislada, nunca sobrescribir producción durante una prueba. El downgrade inicial elimina únicamente tablas ORIENTA; no ejecutarlo sobre una entrega con datos que se quieran conservar.

Después de `upgrade head` e importar catálogo, ejecutar `PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.import_directory` y `PYTHONPATH=backend uv run python -m app.adapters.inbound.cli.review_offers data/revisiones_ofertas.json`. Configurar las dos variables Gemini en el alojamiento del backend; la clave no se distribuye por Git ni a través del frontend. La revisión de cuotas debe repetirse cuando se publique un nuevo periodo.
