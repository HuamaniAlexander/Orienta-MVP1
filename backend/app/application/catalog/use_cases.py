import hashlib
import json
from decimal import Decimal


class CatalogService:
    def __init__(self, repository):
        self.repository = repository

    def detail(self, code):
        career = self.repository.get_career(code)
        offers = self.repository.list_offers(code)
        content = career["content"]
        programs = self.repository.list_programs(code)
        costs = [
            Decimal(value)
            for offer in offers
            for value in (offer["cost"], offer.get("cost_min"), offer.get("cost_max"))
            if offer["cost_status"] == "verificado" and value is not None and Decimal(value) > 0
        ]
        for program in programs:
            if program.get("tuition"):
                costs.extend(Decimal(str(program["tuition"][key])) for key in ("min", "max"))
        months = sorted(
            {o["months"] for o in offers} | {p["months"] for p in programs if p.get("months")}
        )
        duration = " / ".join(f"{n // 12} años" if n % 12 == 0 else f"{n} meses" for n in months)
        # Los costos institucionales y sus estados se conservan, sin presentarlos como precio universal.
        if costs:
            private_cost = (
                f"S/ {min(costs):,.2f}"
                if min(costs) == max(costs)
                else f"S/ {min(costs):,.2f}–{max(costs):,.2f}"
            )
            cost = "Cuotas publicadas: " + private_cost
            if any(o["cost"] is not None and Decimal(o["cost"]) == 0 for o in offers):
                cost = "Públicas: enseñanza gratuita condicionada · " + cost
        else:
            cost = (
                "Enseñanza gratuita condicionada"
                if any(o["cost"] is not None and Decimal(o["cost"]) == 0 for o in offers)
                else "Consultar tarifas por institución y modalidad"
            )
        comparison = {
            k: content.get(k, "Explorar plan institucional")
            for k in (
                "description",
                "courses",
                "activities",
                "skills",
                "specialties",
                "practice",
                "investment",
                "environment",
            )
        }
        comparison.update(
            field=content.get("field")
            or " / ".join(dict.fromkeys(o["detail"].get("campo_laboral", "") for o in offers)),
            duration=duration,
            qualification=content.get(
                "qualification", "Bachiller y título profesional según el programa"
            ),
            cost=cost,
        )
        return {
            **career,
            "version": hashlib.sha256(
                json.dumps(
                    {"base": career["version"], "offers": offers, "programs": programs},
                    sort_keys=True,
                    ensure_ascii=False,
                ).encode()
            ).hexdigest(),
            "offers": offers,
            "institutional_programs": programs,
            "comparison": comparison,
            "cost_note": "Consulta el periodo, la modalidad y el alcance de cada cuota institucional",
            "curriculum_note": "Síntesis general. La malla específica corresponde a cada institución.",
            "sources": list(dict.fromkeys(o["detail"].get("fuente_carrera", "") for o in offers)),
        }
