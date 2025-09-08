from .weather import router as weather_router
# from .crops import router as crops_router
# from .knowledge import router as knowledge_router
from .validation import router as validation_router

__all__ = ['weather_router', 'validation_router']
