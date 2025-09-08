from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    AGROMONITORING_API_KEY: str = ""
    WEATHER_COMPANY_API_KEY: str = ""

    # API Base URLs
    AGROMONITORING_BASE_URL: str = "http://api.agromonitoring.com/agro/1.0"
    WEATHER_COMPANY_BASE_URL: str = "https://api.weather.com/v2"

    # Application Settings
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # CORS Settings
    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    # Cache Settings
    CACHE_TTL: int = 3600

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
