# Pruebas y resultados

La suite cubre: doble importación, equivalencias históricas, dry-run, rollback intermedio, filtros AND, comodines de búsqueda, preservación de costo cero/estimado, 12 criterios y pares inválidos; ausencia de puntuación sin perfil revisado; independencia entre interés y presupuesto; cambio de versión; fallback Gemini; CSRF/origen, hash de contraseñas, cookie, revocación, acceso A/B e idempotencia.

Las pruebas de ML usan escenarios sintéticos solamente para validar separación de participantes y contrato de features; no se publican como métricas predictivas.

Las pruebas frontend verifican errores HTTP, token CSRF antes del guardado y estado accesible de selección. Playwright recorre invitado → comparación → cuestionario → resultado → registro/login → guardado → historial → borrado, además del vacío de búsqueda móvil.

Resultados locales y CI se registran en docs/verification.md al terminar. No confundir pruebas rápidas SQLite con PostgreSQL. CI ejecuta TEST_DATABASE_URL usando un servicio PostgreSQL; cada caso tiene esquema aleatorio propio.

Definition of Done: aceptación implementada, revisión, verificaciones relevantes ejecutadas, documentación actualizada y secretos ausentes. Datos de prueba de cuentas solo en base aislada. No crear cuentas ficticias en el proyecto remoto compartido.
