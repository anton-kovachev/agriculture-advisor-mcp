from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # Weather API Configuration
    AGROMONITORING_API_KEY: str = ""
    AGROMONITORING_BASE_URL: str = "http://api.agromonitoring.com/agro/1.0"
    WEATHER_COMPANY_API_KEY: Optional[str] = ""
    WEATHER_COMPANY_BASE_URL: str = "https://api.weather.com/v2"

    # MCP Server Configuration
    MCP_SERVER_NAME: str = "Agriculture MCP"
    MCP_SERVER_VERSION: str = "2.0.0"
    MCP_SERVER_DESCRIPTION: str = "Expert agricultural guidance for corn, wheat, and sunflower cultivation"

    # Application Settings
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Cache Settings
    CACHE_TTL: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore extra fields from .env
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
