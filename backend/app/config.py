from typing import List, Dict, Any
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://aiuser:aipass@localhost:5432/aiplatform"
    SECRET_KEY: str = "CHANGE_ME_RANDOM_SECRET_DO_NOT_USE_IN_PROD"
    TRUSTED_PROXIES: List[str] = []  # Default empty list - no trusted proxies, only use request.client.host, ignore X-Forwarded-For

    # Payment - Part 3A
    PAYMENT_PROVIDER: str = "sandbox_mock"  # sandbox_mock (default), zarinpal (future 3B), crypto_trc20 (3C), crypto_ton
    EXCHANGE_RATE_TOMAN_PER_USD: int = 190600  # Toman per USD snapshot

    # Credit packages - defined in config not hardcoded in code per spec
    CREDIT_PACKAGES: List[Dict[str, Any]] = [
        {
            "id": "basic_monthly",
            "name_fa": "پایه ماهانه",
            "credits": 1000,
            "price_toman": 299000,
            "price_usd_cents": 200
        },
        {
            "id": "pro_monthly",
            "name_fa": "حرفه‌ای ماهانه",
            "credits": 5000,
            "price_toman": 699000,
            "price_usd_cents": 500
        },
        {
            "id": "creator_monthly",
            "name_fa": "سازنده ماهانه",
            "credits": 15000,
            "price_toman": 1990000,
            "price_usd_cents": 1200
        }
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
