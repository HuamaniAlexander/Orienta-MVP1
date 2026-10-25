# Backlog de referencia

64 tarjetas propuestas; este archivo no afirma que todas estén completadas. La recolección/etiquetado ML, validación experta, revisión institucional, pruebas con usuarios y despliegue externo siguen requiriendo trabajo y evidencia reales. Trello no fue modificado.

## Anexo A. Backlog detallado de 64 tarjetas

### T01. Acordar alcance ampliado y trazabilidad

| Campo | Contenido |
|---|---|
| Módulo / sprint | Gestión / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | — |
| Rama sugerida | `feature/base-configuracion` |
| Descripción | Actualizar MoSCoW e historias al adelantar cuestionario y guardado. |
| Checklist | Revisar APF2; registrar decisión; mapear HU antiguas/nuevas |
| Criterio de aceptación | Documento identifica funciones adelantadas sin renumerar HU existentes. |

### T02. Preparar monorepo y entornos reproducibles

| Campo | Contenido |
|---|---|
| Módulo / sprint | Configuración / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T01 |
| Rama sugerida | `feature/base-configuracion` |
| Descripción | Definir estructura frontend/backend/ML y configuración de desarrollo. |
| Checklist | Crear carpetas; bloquear dependencias; documentar variables ficticias |
| Criterio de aceptación | Otro integrante instala y arranca ambos servicios siguiendo README. |

### T03. Documentar puertos y dependencias hexagonales

| Campo | Contenido |
|---|---|
| Módulo / sprint | Arquitectura / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T01, T02 |
| Rama sugerida | `feature/base-configuracion` |
| Descripción | Definir qué reglas son puras y qué componentes implementan puertos. |
| Checklist | Diagramar; asignar repositorios; registrar composición |
| Criterio de aceptación | Dominio no importa FastAPI, SQLAlchemy, scikit-learn ni SDK externo. |

### T04. Publicar contratos iniciales OpenAPI

| Campo | Contenido |
|---|---|
| Módulo / sprint | API / S1 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T01, T03 |
| Rama sugerida | `feature/base-configuracion` |
| Descripción | Fijar DTO, códigos de error y ejemplos para trabajo paralelo. |
| Checklist | Definir schemas; revisar dinero/fechas; acordar errores |
| Criterio de aceptación | Frontend y backend usan los mismos campos y errores en fixtures. |

### T05. Configurar checks de integración

| Campo | Contenido |
|---|---|
| Módulo / sprint | Calidad / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T02 |
| Rama sugerida | `feature/base-configuracion` |
| Descripción | Ejecutar formato/lint y pruebas existentes en PR. |
| Checklist | Crear workflow; excluir secretos; probar fallo controlado |
| Criterio de aceptación | Un PR con error de verificación no cumple checks de integración. |

### T06. Comprobar conexión PostgreSQL de InsForge

| Campo | Contenido |
|---|---|
| Módulo / sprint | Infraestructura / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T02 |
| Rama sugerida | `feature/datos-esquema` |
| Descripción | Probar conexión real del backend al proyecto con credenciales privadas. |
| Checklist | Obtener cadena por canal seguro; validar TLS; ejecutar SELECT 1 |
| Criterio de aceptación | La conexión funciona sin SDK frontend y los logs no muestran secretos. |

### T07. Auditar y congelar diccionarios heredados

| Campo | Contenido |
|---|---|
| Módulo / sprint | Datos / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T01 |
| Rama sugerida | `feature/datos-importador` |
| Descripción | Guardar las 18 correspondencias actuales como contrato de migración. |
| Checklist | Extraer mapas; detectar colisiones; versionar fixture sin secretos |
| Criterio de aceptación | C01–C19 y códigos 0–18, instituciones y modalidades conservan significado. |

### T08. Definir programas, alias, sedes y ofertas

| Campo | Contenido |
|---|---|
| Módulo / sprint | Datos / S1 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T03, T07 |
| Rama sugerida | `feature/datos-esquema` |
| Descripción | Separar entidades manteniendo IDs originales de oferta y nombres alias. |
| Checklist | Diseñar FK; definir alias; revisar clave de plan/turno |
| Criterio de aceptación | Modelo representa dos modalidades de un programa sin duplicar su perfil académico. |

### T09. Crear migraciones de catálogo y evidencias

| Campo | Contenido |
|---|---|
| Módulo / sprint | Base de datos / S1 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T06, T08 |
| Rama sugerida | `feature/datos-esquema` |
| Descripción | Implementar tablas e índices del catálogo con restricciones. |
| Checklist | Escribir upgrade; revisar downgrade de pruebas; validar null/cero |
| Criterio de aceptación | Migraciones aplican en BD vacía y rechazan duraciones negativas/códigos duplicados. |

### T10. Crear migraciones de cuentas e historial

| Campo | Contenido |
|---|---|
| Módulo / sprint | Base de datos / S1 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T08, T09 |
| Rama sugerida | `feature/datos-esquema` |
| Descripción | Agregar usuarios, sesiones, respuestas, comparación y versiones. |
| Checklist | Definir FK; añadir unicidad por usuario/clave; definir cascadas |
| Criterio de aceptación | Una comparación no admite ofertas iguales y su borrado elimina datos vinculados. |

### T11. Diseñar formato extendido de Excel

| Campo | Contenido |
|---|---|
| Módulo / sprint | Datos / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T07, T08 |
| Rama sugerida | `feature/datos-importador` |
| Descripción | Documentar hojas nuevas, campos de costo y columnas conservadas. |
| Checklist | Mantener hoja original; definir diccionario; ejemplificar rango sin monto |
| Criterio de aceptación | Documento conserva los 38 campos e identifica nuevos campos sin recodificación. |

### T12. Construir lector y validador de importación

| Campo | Contenido |
|---|---|
| Módulo / sprint | Importación / S1 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T07, T11 |
| Rama sugerida | `feature/datos-importador` |
| Descripción | Leer Excel y producir errores por fila antes de persistir. |
| Checklist | Validar columnas; contrastar mapas históricos; revisar números/fechas |
| Criterio de aceptación | Archivo con un código reasignado se rechaza aun si es consistente internamente. |

### T13. Implementar dry-run del catálogo

| Campo | Contenido |
|---|---|
| Módulo / sprint | Importación / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T12 |
| Rama sugerida | `feature/datos-importador` |
| Descripción | Informar altas, cambios y advertencias sin escribir. |
| Checklist | Calcular diff; resumir errores; retornar código de salida |
| Criterio de aceptación | Conteos de BD son iguales antes y después de ejecutar dry-run. |

### T14. Implementar upsert transaccional del lote

| Campo | Contenido |
|---|---|
| Módulo / sprint | Importación / S1 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T09, T12, T13 |
| Rama sugerida | `feature/datos-importador` |
| Descripción | Guardar entidades relacionadas en una transacción única. |
| Checklist | Ordenar FK; usar IDs estables; registrar revisiones solo con cambios |
| Criterio de aceptación | Dos cargas iguales dejan 19 ofertas sin duplicados ni revisiones innecesarias. |

### T15. Verificar rollback y cambios de códigos

| Campo | Contenido |
|---|---|
| Módulo / sprint | Pruebas de datos / S1 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T14 |
| Rama sugerida | `feature/datos-importador` |
| Descripción | Probar error intermedio y consistencia de la migración. |
| Checklist | Introducir fila inválida; ejecutar lote; verificar identidad y contenido |
| Criterio de aceptación | El fallo no deja altas ni cambios parciales de ofertas o diccionarios. |

### T16. Revisar fichas e incorporar ofertas técnicas

| Campo | Contenido |
|---|---|
| Módulo / sprint | Contenido / S1 |
| Prioridad / esfuerzo | P0 / 5 puntos |
| Dependencias | T11, T13 |
| Rama sugerida | `feature/datos-importador` |
| Descripción | Revisar fuentes, costos/modalidades y añadir ofertas técnicas reales. |
| Checklist | Asignar revisor; consultar fuentes; registrar estado/fecha; cargar por CLI |
| Criterio de aceptación | Cada oferta publicada tiene tipo y trazabilidad; existen ofertas técnicas verificadas para demostrar el filtro. |

### T17. Implementar repositorio de catálogo

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend catálogo / S2 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T09, T14 |
| Rama sugerida | `feature/catalogo-api` |
| Descripción | Consultar solo ofertas publicadas y devolver DTO de lectura. |
| Checklist | Mapear entidades; parametrizar SQL; manejar oferta retirada |
| Criterio de aceptación | C01 se recupera con fuentes/estados y un ID desconocido devuelve ausencia controlada. |

### T18. Implementar listado, búsqueda y filtros AND

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend catálogo / S2 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T04, T17 |
| Rama sugerida | `feature/catalogo-api` |
| Descripción | Combinar nombre, tipo, ubicación, modalidad y paginación. |
| Checklist | Validar query; aplicar filtros conjuntos; ordenar de forma estable |
| Criterio de aceptación | Prueba con dos filtros devuelve solo intersección y total consistente. |

### T19. Implementar instituciones y filtros disponibles

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend instituciones / S2 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T17, T18 |
| Rama sugerida | `feature/catalogo-api` |
| Descripción | Exponer instituciones, sedes y opciones disponibles en catálogo. |
| Checklist | Crear list/detail; validar códigos; devolver tipos presentes |
| Criterio de aceptación | No se inventan institutos o modalidades no publicados para llenar controles. |

### T20. Construir cliente HTTP y estados compartidos

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend base / S2 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T04 |
| Rama sugerida | `feature/catalogo-ui` |
| Descripción | Centralizar errores y componentes de carga/vacío. |
| Checklist | Tipar contratos; manejar no-2xx; crear SourceBadge/FeedbackState |
| Criterio de aceptación | Un error 503 se presenta como mensaje recuperable sin mostrar datos de ejemplo como reales. |

### T21. Construir catálogo con filtros persistentes en URL

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend catálogo / S2 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T18, T19, T20 |
| Rama sugerida | `feature/catalogo-ui` |
| Descripción | Mostrar tarjetas y filtros que puedan limpiarse y compartirse. |
| Checklist | Conectar búsqueda; sincronizar filtros; presentar vacío |
| Criterio de aceptación | Recargar URL con filtros conserva criterios; cero resultados ofrece limpiar. |

### T22. Construir ficha trazable de oferta

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend ficha / S2 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T17, T20 |
| Rama sugerida | `feature/catalogo-ui` |
| Descripción | Mostrar seis criterios, fuentes y calidad por atributo. |
| Checklist | Renderizar costos; distinguir null/cero; enlazar fuentes; tratar 404 |
| Criterio de aceptación | S/775 estimados no aparece como tarifa oficial y costo ausente nunca muestra cero. |

### T23. Construir bandeja de dos selecciones

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend comparación / S2 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T21, T22 |
| Rama sugerida | `feature/comparacion` |
| Descripción | Agregar, quitar y sustituir ofertas desde catálogo/ficha. |
| Checklist | Limitar dos; impedir duplicados; enlazar comparación |
| Criterio de aceptación | Seleccionar tercera oferta solicita sustitución y no borra ambas selecciones. |

### T24. Implementar reglas puras de comparación

| Campo | Contenido |
|---|---|
| Módulo / sprint | Dominio comparación / S2 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T03, T08 |
| Rama sugerida | `feature/comparacion` |
| Descripción | Homogeneizar meses y costos sin convertir mensualidad a total. |
| Checklist | Validar IDs diferentes; conservar estados; definir diferencias comparables |
| Criterio de aceptación | Si falta una cifra no se calcula diferencia monetaria inventada. |

### T25. Exponer preview de comparación

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend comparación / S2 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T04, T17, T24 |
| Rama sugerida | `feature/comparacion` |
| Descripción | Construir respuesta con dos ofertas y seis criterios. |
| Checklist | Validar oferta activa; usar caso de uso; manejar error |
| Criterio de aceptación | Mismo ID devuelve 422 y oferta retirada devuelve 404 controlado. |

### T26. Construir tabla móvil de comparación

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend comparación / S2 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T23, T25 |
| Rama sugerida | `feature/comparacion` |
| Descripción | Presentar pares por criterio y permitir reemplazo. |
| Checklist | Diseñar escritorio; apilar móvil; conservar fuentes; enlazar cuestionario |
| Criterio de aceptación | Se comparan seis criterios sin scroll horizontal obligatorio en pantalla estrecha. |

### T27. Construir Inicio y navegación ligera

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend inicio / S2 |
| Prioridad / esfuerzo | P1 / 1 puntos |
| Dependencias | T20, T21 |
| Rama sugerida | `feature/catalogo-ui` |
| Descripción | Explicar objetivo, límites y acceso al catálogo. |
| Checklist | Crear CTA; añadir navegación; revisar textos orientativos |
| Criterio de aceptación | El usuario accede al catálogo sin cuenta ni recursos audiovisuales obligatorios. |

### T28. Verificar recorrido público y estados límite

| Campo | Contenido |
|---|---|
| Módulo / sprint | Calidad pública / S2 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T16, T18, T21, T22, T26 |
| Rama sugerida | `feature/calidad-e2e` |
| Descripción | Probar catálogo a comparación con datos PostgreSQL. |
| Checklist | Probar vacío; misma oferta; retirada; pérdida de red; fuentes |
| Criterio de aceptación | Se registra evidencia del flujo y los casos límite sin servicios ML/Gemini. |

### T29. Revisar cuestionario y esquema q1

| Campo | Contenido |
|---|---|
| Módulo / sprint | Orientación / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T01, T04 |
| Rama sugerida | `feature/cuestionario` |
| Descripción | Validar lenguaje y mapeo de preguntas con apoyo de orientación. |
| Checklist | Revisar 12 preguntas; probar comprensión; definir no sé/versiones |
| Criterio de aceptación | Esquema publicado documenta dimensiones, condiciones y carácter no psicométrico. |

### T30. Revisar perfiles académicos de carreras

| Campo | Contenido |
|---|---|
| Módulo / sprint | Contenido orientación / S3 |
| Prioridad / esfuerzo | P0 / 5 puntos |
| Dependencias | T16, T29 |
| Rama sugerida | `feature/afinidad-baseline` |
| Descripción | Crear vectores con rúbrica y fuentes para programas publicados. |
| Checklist | Revisar mallas; puntuar seis dimensiones; doble revisión; versionar |
| Criterio de aceptación | Cada perfil usado tiene fuentes/revisores y no deriva de códigos de área arbitrarios. |

### T31. Implementar paquete compartido de features

| Campo | Contenido |
|---|---|
| Módulo / sprint | Dominio/ML / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T29, T30 |
| Rama sugerida | `feature/afinidad-baseline` |
| Descripción | Convertir respuestas a dimensiones y similitudes reproducibles. |
| Checklist | Normalizar 1–5; tratar null; definir cobertura; publicar paquete local |
| Criterio de aceptación | Misma entrada/versión genera mismo orden y valores para entrenamiento e inferencia. |

### T32. Implementar afinidad explicable y empates

| Campo | Contenido |
|---|---|
| Módulo / sprint | Motor baseline / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T31 |
| Rama sugerida | `feature/afinidad-baseline` |
| Descripción | Calcular índice y contribuciones con umbrales versionados. |
| Checklist | Aplicar fórmula; devolver cobertura; manejar empate/perfil ausente |
| Criterio de aceptación | Resultados quedan entre 0–100, no se llaman probabilidades y falta de perfil devuelve null. |

### T33. Implementar reglas de factibilidad

| Campo | Contenido |
|---|---|
| Módulo / sprint | Dominio orientación / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T16, T29 |
| Rama sugerida | `feature/afinidad-baseline` |
| Descripción | Evaluar condiciones por oferta separadas del interés. |
| Checklist | Revisar modalidad/ubicación; tratar rangos/estimados; explicar restricciones |
| Criterio de aceptación | Costo estimado produce por confirmar; presupuesto no altera el índice académico. |

### T34. Implementar plantilla local de razones

| Campo | Contenido |
|---|---|
| Módulo / sprint | Explicación / S3 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T32, T33 |
| Rama sugerida | `feature/afinidad-baseline` |
| Descripción | Generar explicación fiel a contribuciones y evidencias. |
| Checklist | Ordenar factores; explicar faltantes; incluir límites; referenciar evidencia |
| Criterio de aceptación | Cada razón puede rastrearse a una respuesta, perfil o dato de oferta. |

### T35. Exponer cuestionario y recomendaciones

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend orientación / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T04, T29, T32, T33, T34 |
| Rama sugerida | `feature/cuestionario` |
| Descripción | Orquestar cálculo sin persistir invitados ni entrenar en HTTP. |
| Checklist | Validar versión/preguntas; cargar perfiles; aplicar motor; serializar |
| Criterio de aceptación | El endpoint devuelve modo, versiones, índices/faltantes y razones reproducibles. |

### T36. Construir cuestionario interactivo

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend orientación / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T23, T29, T35 |
| Rama sugerida | `feature/cuestionario` |
| Descripción | Presentar pasos, revisión y controles de condiciones. |
| Checklist | Permitir no sé; mantener respuestas; mostrar errores; evitar doble envío |
| Criterio de aceptación | Editar respuesta recalcula y las desconocidas no se convierten en cero. |

### T37. Construir resultado y edición de preferencias

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend resultados / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T26, T35, T36 |
| Rama sugerida | `feature/afinidad-baseline` |
| Descripción | Mostrar afinidad/factibilidad por separado y acceso a fuentes. |
| Checklist | Crear paneles; mostrar empate; permitir volver; tratar perfil pendiente |
| Criterio de aceptación | Usuario puede distinguir índice, dato estimado y condición desconocida. |

### T38. Implementar hash de contraseñas y registro

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend auth / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T10, T04 |
| Rama sugerida | `feature/auth-sesiones` |
| Descripción | Registrar email normalizado con contraseña hasheada. |
| Checklist | Integrar Argon2id; validar longitud; resolver duplicados; excluir hash del DTO |
| Criterio de aceptación | No hay contraseñas en claro; email duplicado se controla y hash no sale en respuesta. |

### T39. Implementar sesiones, login, logout y CSRF

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend auth / S3 |
| Prioridad / esfuerzo | P0 / 5 puntos |
| Dependencias | T38 |
| Rama sugerida | `feature/auth-sesiones` |
| Descripción | Gestionar tokens opacos, cookies y revocación. |
| Checklist | Emitir CSRF; rotar login; almacenar hash; caducar; limitar intentos |
| Criterio de aceptación | Logout invalida sesión; mutación sin CSRF falla y cookie tiene atributos acordados. |

### T40. Construir Login, Registro y acceso protegido

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend auth / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T20, T38, T39 |
| Rama sugerida | `feature/auth-ui` |
| Descripción | Conectar formularios y Mi cuenta con sesión de servidor. |
| Checklist | Cargar CSRF; validar campos; redirigir ruta interna; recuperar error |
| Criterio de aceptación | No se guarda token en localStorage y la comparación pública no exige sesión. |

### T41. Implementar guardado atómico con idempotencia

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend historial / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T10, T35, T39 |
| Rama sugerida | `feature/historial` |
| Descripción | Recalcular y persistir snapshot, respuestas y resultado privado. |
| Checklist | Verificar versión esperada; usar transacción; validar clave/body; registrar propietario |
| Criterio de aceptación | Fallo intermedio no guarda parcial; repetición no duplica y cambio de catálogo se informa. |

### T42. Implementar lectura y eliminación por propietario

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend historial / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T41 |
| Rama sugerida | `feature/historial` |
| Descripción | Listar, abrir y eliminar comparaciones solo del usuario actual. |
| Checklist | Paginar; filtrar usuario; borrar cascadas; devolver 404 ajeno |
| Criterio de aceptación | Usuario A no puede consultar ni eliminar comparación de B alterando UUID. |

### T43. Construir Mi cuenta e historial privado

| Campo | Contenido |
|---|---|
| Módulo / sprint | Frontend historial / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T37, T40, T41, T42 |
| Rama sugerida | `feature/historial` |
| Descripción | Guardar desde resultado, listar, reabrir y borrar desde una página. |
| Checklist | Crear tabs; confirmar borrado; tratar vacío; presentar snapshot/versión |
| Criterio de aceptación | Análisis guardado se reabre con datos originales y el borrado se confirma solo al completar. |

### T44. Implementar feedback voluntario separado

| Campo | Contenido |
|---|---|
| Módulo / sprint | Feedback / S3 |
| Prioridad / esfuerzo | P1 / 2 puntos |
| Dependencias | T42, T43 |
| Rama sugerida | `feature/historial` |
| Descripción | Recoger utilidad sin convertirla automáticamente en etiqueta ML. |
| Checklist | Validar escala; acotar comentario; definir consentimiento; limitar frecuencia |
| Criterio de aceptación | Feedback se almacena separado de evaluación experta y respeta propiedad. |

### T45. Verificar integración orientación/auth/historial

| Campo | Contenido |
|---|---|
| Módulo / sprint | Calidad integración / S3 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T37, T39, T43 |
| Rama sugerida | `feature/calidad-e2e` |
| Descripción | Ejecutar casos de orientación y acceso con PostgreSQL. |
| Checklist | Probar no sé; empate; sin presupuesto; fallo DB; sesión expirada; usuario ajeno |
| Criterio de aceptación | Evidencias registran resultados reales y no hay confirmaciones falsas de guardado. |

### T46. Definir protocolo de recolección y rúbrica experta

| Campo | Contenido |
|---|---|
| Módulo / sprint | Investigación ML / S4; preparación desde S1 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T01, T29 |
| Rama sugerida | `feature/ml-dataset` |
| Descripción | Preparar obtención autorizada de perfiles/etiquetas; iniciar desde S1. |
| Checklist | Definir objetivo y=0/1; documentar indeterminado; revisar consentimiento; reclutar revisores |
| Criterio de aceptación | Rúbrica no usa predicciones ni fórmula baseline para generar la verdad de referencia. |

### T47. Recolectar piloto y adjudicar etiquetas reales

| Campo | Contenido |
|---|---|
| Módulo / sprint | Investigación ML / S4 |
| Prioridad / esfuerzo | P0 / 5 puntos |
| Dependencias | T46, T30 |
| Rama sugerida | `feature/ml-dataset` |
| Descripción | Aplicar cuestionario y revisión independiente antes de modelar. |
| Checklist | Capturar perfiles; evaluar sin predicción; resolver desacuerdos; registrar procedencia |
| Criterio de aceptación | Dataset contiene participantes reales, etiquetas revisadas e indeterminados identificados. |

### T48. Auditar dataset y particiones por participante

| Campo | Contenido |
|---|---|
| Módulo / sprint | ML datos / S4 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T47, T31 |
| Rama sugerida | `feature/ml-dataset` |
| Descripción | Separar grupos y congelar contrato de evaluación. |
| Checklist | Revisar nulos/clases; detectar repetidos; reservar test; registrar hashes |
| Criterio de aceptación | Ningún participante cruza train/test y si faltan clases se declara bloqueo. |

### T49. Preparar notebook reproducible de Colab

| Campo | Contenido |
|---|---|
| Módulo / sprint | ML entrenamiento / S4 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T48 |
| Rama sugerida | `feature/ml-entrenamiento` |
| Descripción | Invocar scripts compartidos con versiones bloqueadas. |
| Checklist | Instalar entorno; cargar CSV revisado; auditar catálogo; fijar semilla |
| Criterio de aceptación | Notebook ejecuta desde cero sin datos sintéticos usados como etiquetas reales. |

### T50. Entrenar tres algoritmos y referencias

| Campo | Contenido |
|---|---|
| Módulo / sprint | ML entrenamiento / S4 |
| Prioridad / esfuerzo | P0 / 5 puntos |
| Dependencias | T49 |
| Rama sugerida | `feature/ml-entrenamiento` |
| Descripción | Comparar logística, árbol, bosque, Dummy y baseline sin tocar test para elegir. |
| Checklist | Usar Pipeline; CV agrupada; limitar grids; fijar umbral baseline en validación |
| Criterio de aceptación | Selección está registrada antes de observar test y no se promete >90%. |

### T51. Evaluar test y documentar errores/model card

| Campo | Contenido |
|---|---|
| Módulo / sprint | ML evaluación / S4 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T50 |
| Rama sugerida | `feature/ml-entrenamiento` |
| Descripción | Reportar métricas reales y utilidad/limitaciones del experimento. |
| Checklist | Matrices; métricas por clase/macro; intervalos por participante; análisis de errores |
| Criterio de aceptación | Informe distingue acuerdo experto de éxito vocacional y declara no promoción si no hay evidencia. |

### T52. Exportar pipeline, manifiesto y versión

| Campo | Contenido |
|---|---|
| Módulo / sprint | MLOps mínimo / S4 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T51 |
| Rama sugerida | `feature/ml-integracion` |
| Descripción | Empaquetar un experimento evaluado con metadatos reproducibles. |
| Checklist | Guardar pipeline; calcular hash; listar features; fijar entorno; marcar estado |
| Criterio de aceptación | Artefacto identifica dataset/cuestionario/perfiles y no se declara aprobado por existir. |

### T53. Integrar adaptador ML con puerta de promoción

| Campo | Contenido |
|---|---|
| Módulo / sprint | Backend ML / S4 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T35, T52 |
| Rama sugerida | `feature/ml-integracion` |
| Descripción | Cargar artefacto aprobado una vez por proceso y activar fallback. |
| Checklist | Verificar hash/esquema; probar feature parity; manejar incompatibilidad; registrar modo |
| Criterio de aceptación | Si el modelo no está aprobado o no carga, funciona baseline y no hay entrenamiento por petición. |

### T54. Implementar adaptador Gemini restringido

| Campo | Contenido |
|---|---|
| Módulo / sprint | IA generativa / S4 |
| Prioridad / esfuerzo | P1 / 3 puntos |
| Dependencias | T34, T35 |
| Rama sugerida | `feature/gemini-explicacion` |
| Descripción | Redactar únicamente sobre razones calculadas y catálogo permitido. |
| Checklist | Minimizar payload; definir esquema; validar evidencias; timeout/cuota; configurar key |
| Criterio de aceptación | Ninguna salida modifica scores ni añade cifras; API key permanece en backend. |

### T55. Verificar contingencias Gemini y fidelidad

| Campo | Contenido |
|---|---|
| Módulo / sprint | Pruebas IA / S4 |
| Prioridad / esfuerzo | P1 / 2 puntos |
| Dependencias | T54 |
| Rama sugerida | `feature/gemini-explicacion` |
| Descripción | Comprobar fallos y respuestas no sustentadas. |
| Checklist | Simular 429; timeout; JSON inválido; cifra falsa; evidencia ajena |
| Criterio de aceptación | Todos los casos devuelven plantilla fiel manteniendo comparación y estado útil. |

### T56. Ejecutar flujo completo en navegador

| Campo | Contenido |
|---|---|
| Módulo / sprint | Calidad E2E / S5 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T28, T45 |
| Rama sugerida | `feature/calidad-e2e` |
| Descripción | Validar recorrido público y privado contra backend integrado. |
| Checklist | Invitado compara; responde; registra/login; guarda; reabre; elimina |
| Criterio de aceptación | Registro de ejecución incluye commit, entorno y capturas de casos relevantes. |

### T57. Revisar seguridad y autorización

| Campo | Contenido |
|---|---|
| Módulo / sprint | Seguridad / S5 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T39, T42, T56 |
| Rama sugerida | `feature/calidad-e2e` |
| Descripción | Auditar secretos, cookies, CSRF y acceso a objetos. |
| Checklist | Probar A/B; comprobar bundle; revisar CORS; rate limit; SQL parametrizado |
| Criterio de aceptación | No existe acceso cruzado ni secreto en bundle/logs; defectos críticos corregidos. |

### T58. Validar accesibilidad y comportamiento móvil

| Campo | Contenido |
|---|---|
| Módulo / sprint | UX/calidad / S5 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T26, T36, T37, T43 |
| Rama sugerida | `feature/calidad-e2e` |
| Descripción | Revisar navegación, lectura y estados sin depender del color. |
| Checklist | Usar teclado; revisar labels/contraste; probar pantalla estrecha; ampliar texto |
| Criterio de aceptación | Recorrido principal se completa con teclado y en móvil con criterios legibles. |

### T59. Realizar piloto de comprensión y utilidad

| Campo | Contenido |
|---|---|
| Módulo / sprint | Validación de producto / S5 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T56, T58 |
| Rama sugerida | `feature/calidad-e2e` |
| Descripción | Observar comprensión de comparación, índices y límites. |
| Checklist | Acordar tareas; reclutar voluntarios; registrar observaciones; priorizar defectos |
| Criterio de aceptación | Usuarios intentan identificar diferencias/fuentes/límites y se reportan resultados sin generalización falsa. |

### T60. Preparar despliegue bajo origen común

| Campo | Contenido |
|---|---|
| Módulo / sprint | Infraestructura / S5 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T06, T39, T56 |
| Rama sugerida | `feature/despliegue` |
| Descripción | Publicar versión de prueba con proxy API y configuración privada. |
| Checklist | Configurar HTTPS; aplicar migraciones; empaquetar baseline/modelo aprobado; health checks |
| Criterio de aceptación | React/API/DB funcionan y readiness no depende de Gemini ni Colab abierto. |

### T61. Probar recuperación y rollback de release

| Campo | Contenido |
|---|---|
| Módulo / sprint | Operación / S5 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T60 |
| Rama sugerida | `feature/despliegue` |
| Descripción | Verificar procedimiento de retorno a versión previa y copia DB. |
| Checklist | Crear respaldo de prueba; ensayar restauración aislada; verificar hash; documentar rollback |
| Criterio de aceptación | Equipo demuestra restauración en entorno aislado sin sobrescribir producción. |

### T62. Cerrar documentación y evidencias PDCA

| Campo | Contenido |
|---|---|
| Módulo / sprint | Documentación / S5 |
| Prioridad / esfuerzo | P0 / 3 puntos |
| Dependencias | T15, T45, T56, T57, T59 |
| Rama sugerida | `feature/despliegue` |
| Descripción | Consolidar arquitectura, API, instalación, resultados y mejoras. |
| Checklist | Actualizar README; matriz ponderada; adjuntar pruebas; registrar defecto/corrección |
| Criterio de aceptación | Una HU se traza a CA, commit, prueba ejecutada y mejora con evidencia real. |

### T63. Preparar demostración y video académico

| Campo | Contenido |
|---|---|
| Módulo / sprint | Entrega / S5 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T60, T62 |
| Rama sugerida | `feature/despliegue` |
| Descripción | Explicar flujo y límites con datos del catálogo revisado. |
| Checklist | Escribir guion; mostrar catálogo/comparación; explicar ML real o bloqueo; grabar ≤5 min |
| Criterio de aceptación | Demostración distingue estimados/verificados y no presenta métricas inexistentes. |

### T64. Congelar release y sincronizar ramas

| Campo | Contenido |
|---|---|
| Módulo / sprint | Entrega/Git / S5 |
| Prioridad / esfuerzo | P0 / 2 puntos |
| Dependencias | T57, T58, T61, T62, T63 |
| Rama sugerida | `feature/despliegue` |
| Descripción | Cerrar entrega aprobada e integrar cambios de release a main/dev. |
| Checklist | Revisar checklist; PR release; crear tag; sincronizar dev; registrar pendientes |
| Criterio de aceptación | Tag reproduce la versión demostrada y backlog distingue Done, bloqueado y postergado. |

