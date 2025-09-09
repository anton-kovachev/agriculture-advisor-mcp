"""
Resources module for the Agriculture MCP server.
Provides data access endpoints for agricultural information.
"""

from .weather_resources import WeatherResources

__all__ = ["WeatherResources"]
