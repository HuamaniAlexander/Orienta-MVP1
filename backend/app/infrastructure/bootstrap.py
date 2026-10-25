from types import SimpleNamespace

from app.adapters.outbound.explanation.gemini import GeminiExplainer
from app.adapters.outbound.explanation.template import TemplateExplainer
from app.adapters.outbound.ml.baseline import BaselineEngine
from app.adapters.outbound.persistence.accounts import SqlAccounts, SqlHistory
from app.adapters.outbound.persistence.repositories import SqlCatalogRepository
from app.application.auth.use_cases import AuthService
from app.application.catalog.use_cases import CatalogService
from app.application.history.use_cases import HistoryService
from app.application.orientation.use_cases import OrientationService


def build_services(session, settings, passwords, signal=None):
    catalog = CatalogService(SqlCatalogRepository(session))
    explainer = (
        GeminiExplainer(settings.gemini_api_key, settings.gemini_model)
        if settings.gemini_api_key and settings.gemini_model
        else TemplateExplainer()
    )
    orientation = OrientationService(
        catalog, BaselineEngine(), explainer, settings.demo_mode, signal
    )
    return SimpleNamespace(
        catalog=catalog,
        orientation=orientation,
        auth=AuthService(SqlAccounts(session), passwords, settings.session_hours),
        history=HistoryService(SqlHistory(session), orientation),
    )
