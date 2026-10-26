from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "postgresql+psycopg://orienta:orienta@localhost:5432/orienta"
    app_env: str = "development"
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:8000"]
    cookie_secure: bool = False
    demo_mode: bool = False
    session_hours: int = 8
    gemini_api_key: str = ""
    gemini_model: str = ""
    model_path: str = ""
    content_model_path: str = "data/models/contenido.json"

    def validate_deployment(self):
        if self.app_env == "production" and (not self.cookie_secure or self.demo_mode):
            raise ValueError("Producción exige cookies seguras y DEMO_MODE=false")


@lru_cache
def get_settings():
    settings = Settings()
    settings.validate_deployment()
    return settings
