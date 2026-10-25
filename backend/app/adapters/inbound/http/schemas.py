import re
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PairIn(StrictModel):
    career_ids: list[Annotated[StrictInt, Field(ge=0)]] = Field(min_length=2, max_length=2)

    @model_validator(mode="after")
    def distinct(self):
        if len(set(self.career_ids)) != 2:
            raise ValueError("Selecciona dos carreras distintas")
        return self


class Conditions(StrictModel):
    modalities: list[Literal["Presencial", "Virtual", "Semipresencial"]] = Field(
        default_factory=list, max_length=3
    )
    districts: list[Annotated[str, Field(max_length=80)]] = Field(
        default_factory=list, max_length=10
    )
    monthly_budget: float | None = Field(default=None, ge=0, le=1000000, allow_inf_nan=False)
    max_months: int | None = Field(default=None, ge=1, le=240)
    formation: Literal["cualquiera", "tecnica", "universitaria"] = "cualquiera"


class RecommendationIn(PairIn):
    questionnaire_version: str = Field(max_length=30)
    responses: dict[str, Annotated[StrictInt, Field(ge=1, le=5)] | None] = Field(max_length=8)
    conditions: Conditions = Field(default_factory=Conditions)
    catalog_version: str | None = Field(default=None, max_length=100)


class AuthIn(StrictModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=12, max_length=128)

    @field_validator("email")
    @classmethod
    def valid_email(cls, value):
        value = value.strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            raise ValueError("Ingresa un correo válido")
        return value


class FeedbackIn(StrictModel):
    score: StrictInt = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=500)
    research_consent: bool = False
