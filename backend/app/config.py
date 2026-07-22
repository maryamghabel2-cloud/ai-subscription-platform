from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://aiuser:aipass@localhost:5432/aiplatform"
    SECRET_KEY: str = "CHANGE_ME_RANDOM_SECRET_DO_NOT_USE_IN_PROD"
    TRUSTED_PROXIES: List[str] = []  # Default empty list - no trusted proxies, only use request.client.host, ignore X-Forwarded-For

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
