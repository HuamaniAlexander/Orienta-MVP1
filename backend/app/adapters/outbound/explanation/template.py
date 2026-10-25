LABELS = {"logica": "lógica y análisis", "ciencia": "exploración científica",
          "tecnologia": "soluciones tecnológicas", "personas": "atención a personas",
          "gestion": "organización y gestión", "comunicacion": "creación y comunicación"}


class TemplateExplainer:
    def explain(self, results):
        for result in results:
            factors = sorted(result["affinity"]["contributions"],
                             key=lambda f: f["similarity"], reverse=True)[:3]
            result["reasons"] = [{"id": f"{result['career_id']}:{f['dimension']}",
                                  "text": f"Cercanía entre tus respuestas y las actividades de {LABELS[f['dimension']]}",
                                  "dimension": f["dimension"]} for f in factors]
        return {"mode": "template", "text": "Compara las razones y explora los planes de estudio. La decisión final es tuya."}
