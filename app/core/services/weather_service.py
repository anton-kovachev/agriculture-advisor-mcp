from datetime import datetime, timedelta
from typing import List, Optional
import httpx
from app.core.models.weather import WeatherCondition, WeatherForecast
from app.core.models.location import GeoLocation
from app.config import get_settings

settings = get_settings()


class WeatherService:
    """Service for retrieving weather data from external APIs."""

    def __init__(self):
        self.agro_api_key = settings.AGROMONITORING_API_KEY
        self.weather_api_key = settings.WEATHER_COMPANY_API_KEY
        self.agro_base_url = settings.AGROMONITORING_BASE_URL
        self.weather_base_url = settings.WEATHER_COMPANY_BASE_URL

    async def get_current_weather(self, location: GeoLocation) -> WeatherCondition:
        """Get current weather conditions for a location."""
        async with httpx.AsyncClient() as client:
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.agro_api_key
            }

            response = await client.get(f"{self.agro_base_url}/weather", params=params)
            response.raise_for_status()
            data = response.json()

            return WeatherCondition(
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                precipitation=data["rain"]["1h"] if "rain" in data else 0.0,
                wind_speed=data["wind"]["speed"],
                wind_direction=data["wind"]["deg"],
                timestamp=datetime.utcfromtimestamp(data["dt"])
            )

    async def get_weather_forecast(self, location: GeoLocation, days: int = 7) -> WeatherForecast:
        """Get weather forecast for a location."""
        async with httpx.AsyncClient() as client:
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.agro_api_key,
                "cnt": days * 8  # 3-hour forecasts for the number of days
            }

            response = await client.get(f"{self.agro_base_url}/forecast", params=params)
            response.raise_for_status()
            data = response.json()

            forecast_data = []
            for item in data["list"]:
                forecast_data.append(
                    WeatherCondition(
                        temperature=item["main"]["temp"],
                        humidity=item["main"]["humidity"],
                        precipitation=item["rain"]["3h"] if "rain" in item else 0.0,
                        wind_speed=item["wind"]["speed"],
                        wind_direction=item["wind"]["deg"],
                        timestamp=datetime.utcfromtimestamp(item["dt"])
                    )
                )

            return WeatherForecast(
                location_id=f"{location.latitude},{location.longitude}",
                forecast_data=forecast_data
            )

    async def get_soil_data(self, location: GeoLocation) -> dict:
        """Get soil data for a location."""
        async with httpx.AsyncClient() as client:
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.agro_api_key
            }

            response = await client.get(f"{self.agro_base_url}/soil", params=params)
            response.raise_for_status()
            return response.json()
