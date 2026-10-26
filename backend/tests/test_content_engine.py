import json
from pathlib import Path

import pytest
from app.adapters.outbound.ml.content_engine import ANCHORS, ContentEngine
from sklearn.feature_extraction.text import TfidfVectorizer

from ml.src.train_content import STOP_WORDS, train


def test_runtime_matches_fitted_vectorizer(tmp_path):
    corpus = Path("data/ml/corpus_carreras.json")
    artifact = tmp_path / "content.json"
    report = train(corpus, artifact)
    assert report["documents"] == 13 and report["supervised"] is False
    model = ContentEngine(artifact)
    docs = json.loads(corpus.read_text())
    fitted = TfidfVectorizer(
        strip_accents="unicode", ngram_range=(1, 2), sublinear_tf=True, stop_words=STOP_WORDS
    )
    fitted.fit(r["text"] for r in docs)
    for _, text in ANCHORS.values():
        expected = fitted.transform([text])
        actual = model.transform(text)
        assert actual == pytest.approx({int(i): float(expected[0, i]) for i in expected.indices})


def test_content_changes_with_actual_interests_and_keeps_unknowns():
    model = ContentEngine("data/models/contenido.json")
    responses = {f"Q{i:02}": 1 for i in range(1, 9)}
    responses["Q03"] = 5
    assert model.evaluate(responses, 0)["score"] > model.evaluate(responses, 6)["score"]
    responses["Q03"] = 1
    responses["Q04"] = 5
    assert model.evaluate(responses, 6)["score"] > model.evaluate(responses, 0)["score"]
    assert model.evaluate({k: None for k in responses}, 0)["score"] is None
    assert model.evaluate({k: 1 for k in responses}, 0)["score"] is None


def test_content_artifact_tampering_rejected(tmp_path):
    raw = Path("data/models/contenido.json").read_bytes()
    (tmp_path / "model.json").write_bytes(raw + b" ")
    (tmp_path / "model.manifest.json").write_bytes(
        Path("data/models/contenido.manifest.json").read_bytes()
    )
    with pytest.raises(ValueError, match="manifest"):
        ContentEngine(tmp_path / "model.json")


def test_live_recommendation_has_content_evidence_without_unreviewed_affinity(client, payload):
    client.app.state.settings.demo_mode = False
    result = client.post("/api/v1/recomendaciones", json=payload).json()
    assert result["mode"] == "content_based"
    assert all(item["affinity"]["index"] is None for item in result["results"])
    assert all(
        item["content_match"]["score"] is not None and item["reasons"] for item in result["results"]
    )


def test_budget_preserves_ranges_and_does_not_guess_the_student_scale():
    from app.domain.orientation.feasibility import program_budget

    program = {"tuition": {"min": 1000, "max": 2000}}
    assert program_budget(program, {"monthly_budget": 900}) == "incompatible"
    assert program_budget(program, {"monthly_budget": 1500}) == "depends_on_scale"
    assert program_budget(program, {"monthly_budget": 2000}) == "compatible"
