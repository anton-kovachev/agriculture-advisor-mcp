import os
from typing import Optional


class Settings:
    """Application settings and configuration."""

    # MCP Server Configuration
    MCP_SERVER_NAME: str = "Agriculture MCP"
    MCP_SERVER_VERSION: str = "2.0.0"

    # Weather API Configuration
    OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
    WEATHER_API_TIMEOUT: int = 10  # seconds
    WEATHER_CACHE_TTL: int = 300   # 5 minutes in seconds

    # Agricultural Data Configuration
    DEFAULT_CROP_TYPES: list = ["corn", "wheat", "sunflower"]
    DEFAULT_SOIL_TYPES: list = ["clay", "loam", "sandy", "silt"]

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    # Development settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    @property
    def has_weather_api_key(self) -> bool:
        """Check if weather API key is configured."""
        return bool(self.OPENWEATHER_API_KEY)


settings = Settings()
