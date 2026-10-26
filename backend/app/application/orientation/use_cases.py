import hashlib
from app.domain.comparison.rules import check_pair, comparison_rows
from app.domain.errors import DomainError
from app.domain.orientation.affinity import preference
from app.domain.orientation.feasibility import feasibility

QUESTIONS = [
    ("Q01", "¿Cuánto te interesa resolver problemas con números y lógica?"),
    ("Q02", "¿Cuánto disfrutas explorar fenómenos mediante evidencia?"),
    ("Q03", "¿Cuánto te interesa crear o entender soluciones tecnológicas?"),
    ("Q04", "¿Cuánto te gustaría contribuir al bienestar de otras personas?"),
    ("Q05", "¿Cuánto te interesa organizar recursos y coordinar actividades?"),
    ("Q06", "¿Cuánto disfrutas diseñar, comunicar o crear propuestas?"),
    ("Q07", "¿Cuánto te interesan el análisis y la experimentación?"),
    ("Q08", "¿Cuánto te interesa colaborar y presentar ideas?"),
]


class OrientationService:
    def __init__(self, catalog, engine, explainer, demo=False, signal=None):
        self.catalog, self.engine, self.explainer = catalog, engine, explainer
        self.demo, self.signal = demo, signal

    def preview(self, ids):
        check_pair(ids)
        careers = [self.catalog.detail(code) for code in ids]
        return {
            "careers": careers,
            "criteria": comparison_rows(careers),
            "catalog_version": hashlib.sha256("|".join(c["version"] for c in careers).encode()).hexdigest(),
        }

    def recommend(self, payload):
        if payload["questionnaire_version"] != "q1":
            raise DomainError("El cuestionario cambió. Vuelve a cargarlo.", "version_conflict", 409)
        responses = payload["responses"]
        if set(responses) != {q[0] for q in QUESTIONS}:
            raise DomainError("Responde las ocho preguntas o marca Aún no lo sé")
        preview = self.preview(payload["career_ids"])
        expected = payload.get("catalog_version")
        if expected and expected != preview["catalog_version"]:
            raise DomainError(
                "El catálogo cambió. Revisa la nueva comparación antes de guardar.",
                "version_conflict",
                409,
            )
        results = []
        for career in preview["careers"]:
            approved = career["profile_reviewed"]
            if career["profile"] and (approved or self.demo):
                affinity = self.engine.evaluate(responses, career["profile"])
            else:
                affinity = {"index": None, "coverage": 0, "dimensions": 6, "contributions": []}
            signal = None
            if self.signal and approved and affinity["coverage"] == 6:
                signal = self.signal.predict(responses, career["profile"])
            results.append(
                {
                    "career_id": career["id"],
                    "name": career["name"],
                    "affinity": affinity,
                    "expert_label_estimate": signal,
                    "profile_status": "reviewed"
                    if approved
                    else "illustrative"
                    if self.demo
                    else "requires_review",
                    "comparison": career["comparison"],
                    "offers": [
                        {**o, "feasibility": feasibility(o, payload.get("conditions", {}))}
                        for o in career["offers"]
                    ],
                }
            )
        explanation = self.explainer.explain(
            results,
            {
                "responses": responses,
                "conditions": payload.get("conditions", {}),
                "questions": dict(QUESTIONS),
            },
        )
        return {
            "mode": "ml_complementary" if self.signal else "baseline",
            "engine_version": self.engine.version,
            "questionnaire_version": "q1",
            "catalog_version": preview["catalog_version"],
            "demo": self.demo,
            "results": results,
            "preference": preference(results),
            "explanation": explanation,
            "notice": "Índice orientativo, no probabilidad de éxito. La decisión es tuya.",
            "saved": False,
        }
