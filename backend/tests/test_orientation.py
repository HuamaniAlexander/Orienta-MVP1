from app.adapters.outbound.explanation.gemini import GeminiExplainer
from app.domain.orientation.affinity import affinity


def test_formula_matches_documented_example():
    # Las similitudes se prueban con datos sintéticos de software, no con etiquetas ML.
    response = {f"Q{i:02}": 5 for i in range(1, 9)}
    assert affinity(response, [1] * 6)["index"] == 100
    assert affinity(response, [0] * 6)["index"] == 0


def test_unknown_is_not_zero():
    score = affinity({f"Q{i:02}": None for i in range(1, 9)}, [0.5] * 6)
    assert score["index"] is None and score["coverage"] == 0


def test_budget_does_not_change_interest_score(client, payload):
    first = client.post("/api/v1/recomendaciones", json=payload).json()
    payload["conditions"]["monthly_budget"] = 10
    second = client.post("/api/v1/recomendaciones", json=payload).json()
    assert first["results"][0]["affinity"] == second["results"][0]["affinity"]
    assert first["results"][0]["offers"][0]["feasibility"]["budget"] == "review_source"


def test_invalid_question_and_version(client, payload):
    payload["questionnaire_version"] = "q0"
    assert client.post("/api/v1/recomendaciones", json=payload).status_code == 409
    payload["questionnaire_version"] = "q1"
    payload["responses"]["Q99"] = payload["responses"].pop("Q01")
    assert client.post("/api/v1/recomendaciones", json=payload).status_code == 422


def test_no_unreviewed_scores_in_live_mode(client, payload):
    client.app.state.settings.demo_mode = False
    result = client.post("/api/v1/recomendaciones", json=payload).json()
    assert all(c["affinity"]["index"] is None for c in result["results"])
    assert result["preference"]["career_id"] is None


def test_changed_catalog_rejected(client, payload):
    payload["catalog_version"] = "antigua"
    assert client.post("/api/v1/recomendaciones", json=payload).status_code == 409


def test_gemini_fallback_does_not_invent(monkeypatch):
    def fail(*args, **kwargs):
        import httpx

        raise httpx.TimeoutException("simulado")

    monkeypatch.setattr("httpx.post", fail)
    results = [{"career_id": 0, "affinity": {"contributions": []}}]
    explanation = GeminiExplainer("dummy", "model").explain(results)
    assert explanation["mode"] == "template" and results[0]["reasons"] == []
