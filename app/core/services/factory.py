"""Service factory functions for dependency injection."""
from functools import lru_cache
from app.config import get_settings
from app.core.services.weather_service import WeatherService
from app.core.services.crop_service import CropManagementService
from app.core.services.knowledge_service import KnowledgeBaseService


@lru_cache()
def get_weather_service() -> WeatherService:
    """Create and configure a WeatherService instance."""
    return WeatherService()


@lru_cache()
def get_crop_service(
    weather_service: WeatherService = get_weather_service()
) -> CropManagementService:
    """Create and configure a CropManagementService instance."""
    return CropManagementService(weather_service)


@lru_cache()
def get_knowledge_service() -> KnowledgeBaseService:
    """Create and configure a KnowledgeBaseService instance."""
    return KnowledgeBaseService()
