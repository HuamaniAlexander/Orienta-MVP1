from decimal import Decimal


class CatalogService:
    def __init__(self, repository):
        self.repository = repository

    def detail(self, code):
        career = self.repository.get_career(code)
        offers = self.repository.list_offers(code)
        content = career["content"]
        costs = [Decimal(o["cost"]) for o in offers if o["cost"] is not None and Decimal(o["cost"]) > 0]
        months = sorted({o["months"] for o in offers})
        duration = " / ".join(f"{n // 12} años" if n % 12 == 0 else f"{n} meses" for n in months)
        # Los costos institucionales y sus estados se conservan, sin presentarlos como precio universal.
        cost = f"S/ {min(costs):,.0f}–{max(costs):,.0f}" if costs else "Ver instituciones públicas y privadas"
        comparison = {k: content.get(k, "Explorar plan institucional") for k in (
            "description", "courses", "activities", "skills", "specialties", "practice", "investment", "environment")}
        comparison.update(field=" / ".join(dict.fromkeys(o["detail"].get("campo_laboral", "") for o in offers)),
                          duration=duration, qualification="Bachiller y título profesional según el programa", cost=cost)
        return {**career, "offers": offers, "comparison": comparison,
                "cost_note": "Referencia del catálogo; consulta el estado y alcance en cada institución",
                "curriculum_note": "Síntesis general. La malla específica corresponde a cada institución.",
                "sources": list(dict.fromkeys(o["detail"].get("fuente_carrera", "") for o in offers))}
