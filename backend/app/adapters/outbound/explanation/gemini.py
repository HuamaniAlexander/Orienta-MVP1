import json

import httpx

from .template import TemplateExplainer


class GeminiExplainer(TemplateExplainer):
    """Gemini puede ordenar razones existentes; nunca inventar datos o cambiar scores."""

    def __init__(self, api_key, model):
        self.api_key, self.model = api_key, model

    def explain(self, results):
        fallback = super().explain(results)
        bank = [reason for item in results for reason in item["reasons"]]
        try:
            response = httpx.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
                headers={"x-goog-api-key": self.api_key},
                timeout=5,
                json={
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": "Ordena estas razones por claridad. Devuelve solo JSON con ordered_ids. No añadas ids. "
                                    + json.dumps(bank, ensure_ascii=False)
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "responseMimeType": "application/json",
                        "maxOutputTokens": 300,
                    },
                },
            )
            response.raise_for_status()
            ordered = json.loads(response.json()["candidates"][0]["content"]["parts"][0]["text"])[
                "ordered_ids"
            ]
            if (
                not isinstance(ordered, list)
                or len(ordered) != len(bank)
                or set(ordered) != {r["id"] for r in bank}
            ):
                return fallback
            for item in results:
                item["reasons"].sort(key=lambda reason: ordered.index(reason["id"]))
            return {**fallback, "mode": "gemini_constrained"}
        except (httpx.HTTPError, KeyError, IndexError, ValueError, TypeError):
            return fallback
