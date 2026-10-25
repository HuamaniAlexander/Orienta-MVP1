from typing import Protocol


class CatalogRepository(Protocol):
    def list_careers(self, **filters) -> tuple[list[dict], int]: ...
    def get_career(self, code: int) -> dict: ...
    def list_offers(self, career_code: int | None = None, district: str = "") -> list[dict]: ...


class AffinityEngine(Protocol):
    version: str

    def evaluate(self, responses: dict, profile: list[float]) -> dict: ...


class Explainer(Protocol):
    def explain(self, results: list[dict]) -> dict: ...
