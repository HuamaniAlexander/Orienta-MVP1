from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, Query, Request, Response
from sqlalchemy import text

from app.application.orientation.use_cases import QUESTIONS
from app.domain.errors import DomainError
from app.infrastructure.bootstrap import build_services
from .schemas import AuthIn, FeedbackIn, PairIn, RecommendationIn

router = APIRouter(prefix="/api/v1")
COOKIE = "orienta_session"


def services(request: Request):
    with request.app.state.factory.begin() as session:
        yield build_services(session, request.app.state.settings, request.app.state.passwords, request.app.state.signal)


def set_cookie(response, token, settings):
    response.set_cookie(COOKIE, token, httponly=True, secure=settings.cookie_secure,
                        samesite="lax", max_age=settings.session_hours*3600, path="/")


def check_csrf(request, svc):
    origin = request.headers.get("origin")
    if origin and origin not in request.app.state.settings.allowed_origins and origin != str(request.base_url).rstrip("/"):
        raise DomainError("Origen no autorizado", "origin_invalid", 403)
    return svc.auth.require_csrf(request.cookies.get(COOKIE), request.headers.get("x-csrf-token"))


def current(request, svc):
    return svc.auth.current_user(request.cookies.get(COOKIE))


@router.get("/health/live")
def live():
    return {"status": "ok"}


@router.get("/health/ready")
def ready(request: Request):
    with request.app.state.factory() as session:
        count = session.scalar(text("SELECT count(*) FROM orienta.career WHERE active = true"))
        if not count:
            raise DomainError("Catálogo sin cargar", "unavailable", 503)
    return {"status": "ready"}


@router.get("/carreras")
def list_careers(q: str = Query("", max_length=100), area: str = Query("", max_length=100),
                 kind: str = Query("", pattern="^(|universitaria|tecnica)$"), district: str = Query("", max_length=80),
                 page: int = Query(1, ge=1), page_size: int = Query(12, ge=1, le=50), svc=Depends(services)):
    items, total = svc.catalog.repository.list_careers(q=q, area=area, kind=kind, district=district, page=page, page_size=page_size)
    # El vector editorial nunca se envía como una evaluación validada del usuario.
    items = [{k: v for k, v in item.items() if k not in {"profile"}} for item in items]
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/carreras/{code}")
def career(code: int, svc=Depends(services)):
    result = svc.catalog.detail(code)
    result.pop("profile", None)
    return result


@router.get("/catalogo/filtros")
def filters(svc=Depends(services)):
    items, _ = svc.catalog.repository.list_careers(page_size=1000)
    offers = svc.catalog.repository.list_offers()
    return {"areas": sorted({c["area"] for c in items}), "kinds": sorted({c["kind"] for c in items}),
            "districts": sorted({o["district"] for o in offers if o["district"]}),
            "modalities": sorted({o["modality"] for o in offers})}


@router.get("/instituciones")
def institutions(svc=Depends(services)):
    return {"items": svc.catalog.repository.institutions()}


@router.get("/instituciones/{code}")
def institution(code: int, svc=Depends(services)):
    item = next((i for i in svc.catalog.repository.institutions() if i["id"] == code), None)
    if not item:
        raise DomainError("Institución no encontrada", "not_found", 404)
    return item


@router.get("/ofertas")
def offers(career_id: int | None = None, district: str = Query("", max_length=80), svc=Depends(services)):
    return {"items": svc.catalog.repository.list_offers(career_id, district)}


@router.get("/ofertas/{offer_id}")
def offer(offer_id: str, svc=Depends(services)):
    item = next((o for o in svc.catalog.repository.list_offers() if o["id"] == offer_id), None)
    if not item:
        raise DomainError("Oferta no encontrada", "not_found", 404)
    return item


@router.post("/comparaciones/preview")
def preview(payload: PairIn, svc=Depends(services)):
    return svc.orientation.preview(payload.career_ids)


@router.get("/cuestionarios/actual")
def questionnaire():
    return {"version": "q1", "questions": [{"id": key, "text": value} for key, value in QUESTIONS],
            "condition_steps": ["modalidad", "distrito", "presupuesto", "duracion_y_tipo"],
            "notice": "Exploración orientativa, no evaluación psicológica"}


@router.post("/recomendaciones")
def recommendations(payload: RecommendationIn, svc=Depends(services)):
    return svc.orientation.recommend(payload.model_dump())


@router.get("/auth/csrf")
def csrf(request: Request, response: Response, svc=Depends(services)):
    token, csrf_value = svc.auth.csrf(request.cookies.get(COOKIE))
    set_cookie(response, token, request.app.state.settings)
    response.headers["Cache-Control"] = "no-store"
    return {"csrf_token": csrf_value}


@router.post("/auth/registro", status_code=201)
def register(payload: AuthIn, request: Request, svc=Depends(services)):
    check_csrf(request, svc)
    return svc.auth.register(payload.email, payload.password)


@router.post("/auth/login")
def login(payload: AuthIn, request: Request, response: Response, svc=Depends(services)):
    row = check_csrf(request, svc)
    result, token = svc.auth.login(payload.email, payload.password, row)
    set_cookie(response, token, request.app.state.settings)
    return result


@router.get("/auth/me")
def me(request: Request, svc=Depends(services)):
    return current(request, svc)


@router.post("/auth/logout", status_code=204)
def logout(request: Request, response: Response, svc=Depends(services)):
    check_csrf(request, svc)
    svc.auth.logout(request.cookies.get(COOKIE))
    response.delete_cookie(COOKIE, path="/", secure=request.app.state.settings.cookie_secure, httponly=True, samesite="lax")


@router.post("/comparaciones", status_code=201)
def save(payload: RecommendationIn, request: Request, idempotency_key: str = Header(), svc=Depends(services)):
    check_csrf(request, svc); user = current(request, svc)
    try:
        key = str(UUID(idempotency_key))
    except ValueError:
        raise DomainError("Idempotency-Key debe ser UUID") from None
    if not payload.catalog_version:
        raise DomainError("Envía la versión de catálogo que acabas de revisar")
    return svc.history.save(user["id"], key, payload.model_dump())


@router.get("/comparaciones")
def history(request: Request, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=50), svc=Depends(services)):
    user = current(request, svc)
    items, total = svc.history.repository.list(user["id"], page, page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/comparaciones/{cid}")
def saved(cid: str, request: Request, svc=Depends(services)):
    user = current(request, svc)
    return svc.history.repository.serialize(svc.history.get(user["id"], cid))


@router.delete("/comparaciones/{cid}", status_code=204)
def delete(cid: str, request: Request, svc=Depends(services)):
    check_csrf(request, svc); user = current(request, svc)
    svc.history.delete(user["id"], cid)


@router.post("/comparaciones/{cid}/feedback", status_code=201)
def feedback(cid: str, payload: FeedbackIn, request: Request, svc=Depends(services)):
    check_csrf(request, svc); user = current(request, svc)
    svc.history.get(user["id"], cid)
    fid = str(uuid4())
    svc.history.repository.feedback(id=fid, comparison_id=cid, **payload.model_dump())
    return {"id": fid, "received": True}
