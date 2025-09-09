import os
from typing import Optional


class Settings:
    """Application settings and configuration."""

    # MCP Server Configuration
    MCP_SERVER_NAME: str = "Agriculture MCP"
    MCP_SERVER_VERSION: str = "2.0.0"
    MCP_SERVER_DESCRIPTION: str = "Expert agricultural guidance for corn, wheat, and sunflower cultivation"

    # Weather API Configuration
    OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
    AGROMONITORING_API_KEY: str = os.getenv("AGROMONITORING_API_KEY", "")
    AGROMONITORING_BASE_URL: str = "http://api.agromonitoring.com/agro/1.0"
    WEATHER_COMPANY_API_KEY: Optional[str] = os.getenv(
        "WEATHER_COMPANY_API_KEY", "")
    WEATHER_COMPANY_BASE_URL: str = "https://api.weather.com/v2"
    WEATHER_API_TIMEOUT: int = 10  # seconds
    WEATHER_CACHE_TTL: int = 300   # 5 minutes in seconds

    # Agricultural Data Configuration
    DEFAULT_CROP_TYPES: list = ["corn", "wheat", "sunflower"]
    DEFAULT_SOIL_TYPES: list = ["clay", "loam", "sandy", "silt"]

    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = "INFO"
    CACHE_TTL: int = 3600

    @property
    def has_weather_api_key(self) -> bool:
        """Check if weather API key is configured."""
        return bool(self.OPENWEATHER_API_KEY or self.AGROMONITORING_API_KEY)


settings = Settings()
