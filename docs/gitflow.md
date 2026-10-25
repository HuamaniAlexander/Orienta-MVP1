# GitFlow

main: base estable. dev: integración. feature/base-configuracion, feature/datos-esquema, feature/datos-importador, feature/catalogo-api, feature/afinidad-baseline, feature/auth-sesiones, feature/historial, feature/api-integracion, feature/catalogo-ui, feature/orientacion-ui, feature/ml-entrenamiento y feature/calidad-e2e documentan los módulos implementados. Las features se construyeron en secuencia porque existen dependencias explícitas.

La entrega consolidada se prepara en release/0.1.0 para PR a main, sin reescribir main. Al trabajar en equipo, partir de dev actualizado y abrir PR pequeños, ejecutar checks y revisar contratos/migraciones. Preservar commits atómicos en español al integrar. No crear ramas vacías para aparentar trabajo.

Protecciones recomendadas: main/dev sin push directo ni force push, CI requerida y revisión de un compañero. No se afirman protecciones activadas si no se configuraron en GitHub. Tag v0.1.0 solo después de aprobar y publicar la release. Hotfix desde main y retorno a dev.
