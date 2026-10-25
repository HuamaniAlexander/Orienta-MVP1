import logging
import time
from collections import OrderedDict, deque
from contextlib import asynccontextmanager
from pathlib import Path
from threading import Lock
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware

from app.adapters.inbound.http.routes import router
from app.adapters.outbound.security.passwords import ArgonPasswords
from app.domain.errors import DomainError
from app.infrastructure.config import get_settings
from app.infrastructure.database import create_database


def create_app(settings=None, database=None):
    settings = settings or get_settings()
    engine, factory = database or create_database(settings.database_url)

    @asynccontextmanager
    async def lifespan(app):
        yield
        engine.dispose()

    app = FastAPI(title="ORIENTA API", version="0.1.0", lifespan=lifespan)
    app.state.settings, app.state.engine, app.state.factory = settings, engine, factory
    app.state.passwords, app.state.signal = ArgonPasswords(), None
    if settings.model_path:
        try:
            from app.adapters.outbound.ml.sklearn_engine import SklearnSignal
            app.state.signal = SklearnSignal(settings.model_path)
        except (ValueError, OSError, ImportError, KeyError):
            logging.getLogger("orienta").warning("Modelo no disponible: se mantiene baseline")
    app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins,
                       allow_credentials=True, allow_methods=["GET", "POST", "DELETE"],
                       allow_headers=["Content-Type", "X-CSRF-Token", "Idempotency-Key"])
    buckets, lock = OrderedDict(), Lock()

    def error(request, status, code, message, fields=None):
        return JSONResponse({"error": {"code": code, "message": message, "fields": fields or [],
                                       "request_id": getattr(request.state, "request_id", "")}}, status_code=status)

    @app.middleware("http")
    async def guard(request: Request, call_next):
        request.state.request_id = str(uuid4())
        if request.url.path.startswith("/api/"):
            category = "auth" if request.url.path.startswith("/api/v1/auth/") else "analysis" if request.url.path.endswith("/recomendaciones") else "general"
            limit = 30 if category in {"auth", "analysis"} else 180
            key = (request.client.host if request.client else "unknown", category)
            stamp = time.monotonic()
            with lock:
                bucket = buckets.setdefault(key, deque())
                buckets.move_to_end(key)
                while bucket and bucket[0] < stamp - 60:
                    bucket.popleft()
                exceeded = len(bucket) >= limit
                if not exceeded:
                    bucket.append(stamp)
                while len(buckets) > 10000:
                    buckets.popitem(last=False)
            if exceeded:
                response = error(request, 429, "rate_limited", "Demasiados intentos. Espera un minuto.")
                response.headers["Retry-After"] = "60"
                return response
            if request.method in {"POST", "DELETE"} and int(request.headers.get("content-length", "0") or 0) > 16384:
                return error(request, 413, "too_large", "Solicitud demasiado grande")
        response = await call_next(request)
        response.headers.update({"X-Request-ID": request.state.request_id,
                                 "X-Content-Type-Options": "nosniff", "Referrer-Policy": "strict-origin-when-cross-origin",
                                 "X-Frame-Options": "DENY", "Permissions-Policy": "camera=(), microphone=(), geolocation=()"})
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(DomainError)
    async def domain_error(request, exc):
        return error(request, exc.status, exc.code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        fields = [{"field": ".".join(str(x) for x in e["loc"]), "message": e["msg"]} for e in exc.errors()]
        return error(request, 422, "validation_error", "Revisa los datos ingresados", fields)

    @app.exception_handler(IntegrityError)
    async def integrity_error(request, exc):
        return error(request, 409, "conflict", "El registro cambió o ya existe. Vuelve a intentar.")

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        return error(request, 503, "database_unavailable", "No se pudo conectar al servicio de datos. Intenta nuevamente.")

    app.include_router(router)
    dist = Path(__file__).resolve().parents[1] / "frontend" / "dist"
    if dist.exists():
        app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

        @app.get("/{path:path}", include_in_schema=False)
        def frontend(path: str):
            if path.startswith("api/"):
                return JSONResponse({"error": {"code": "not_found", "message": "Ruta no encontrada"}}, status_code=404)
            return FileResponse(dist / "index.html")
    return app


app = create_app()
