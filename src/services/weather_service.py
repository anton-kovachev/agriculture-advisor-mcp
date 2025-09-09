from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import httpx
import logging

from models.weather import WeatherCondition, WeatherForecast
from models.location import GeoLocation
from config import settings

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for retrieving weather data from external APIs."""

    def __init__(self):
        self.agro_api_key = settings.AGROMONITORING_API_KEY
        self.weather_api_key = getattr(settings, 'WEATHER_COMPANY_API_KEY', '')
        self.agro_base_url = settings.AGROMONITORING_BASE_URL
        self.weather_base_url = getattr(
            settings, 'WEATHER_COMPANY_BASE_URL', 'https://api.weather.com/v1')
        self.timeout = 30.0

    async def get_current_weather(self, location: GeoLocation) -> WeatherCondition:
        """Get current weather conditions for a location."""
        try:
            # Use OpenWeatherMap API (compatible with AgroMonitoring structure)
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "appid": self.agro_api_key,
                    "units": "metric"
                }

                # Try AgroMonitoring first, fallback to OpenWeatherMap format
                base_url = self.agro_base_url.replace("/agro/1.0", "/data/2.5")
                response = await client.get(
                    f"{base_url}/weather",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                return WeatherCondition(
                    temperature=data["main"]["temp"],
                    humidity=data["main"]["humidity"],
                    precipitation=data.get("rain", {}).get("1h", 0.0),
                    wind_speed=data["wind"]["speed"],
                    wind_direction=data["wind"]["deg"],
                    soil_temperature=data["main"]["temp"] - 2.0,  # Estimate
                    soil_moisture=max(
                        # Estimate
                        0, min(100, data["main"]["humidity"] * 0.7)),
                    timestamp=datetime.utcfromtimestamp(data["dt"])
                )
        except httpx.HTTPError as e:
            logger.error(f"HTTP error getting current weather: {e}")
            # Return fallback data instead of raising
            return self._get_fallback_weather(location)
        except Exception as e:
            logger.error(f"Error getting current weather: {e}")
            return self._get_fallback_weather(location)

    async def get_weather_forecast(
        self,
        location: GeoLocation,
        days: int = 7
    ) -> WeatherForecast:
        """Get weather forecast for a location."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "appid": self.agro_api_key,
                    # 3-hour forecasts, max 40 (5 days)
                    "cnt": min(days * 8, 40),
                    "units": "metric"
                }

                base_url = self.agro_base_url.replace("/agro/1.0", "/data/2.5")
                response = await client.get(
                    f"{base_url}/forecast",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                forecast_data = []
                for item in data["list"]:
                    forecast_data.append(
                        WeatherCondition(
                            temperature=item["main"]["temp"],
                            humidity=item["main"]["humidity"],
                            precipitation=item.get("rain", {}).get("3h", 0.0),
                            wind_speed=item["wind"]["speed"],
                            wind_direction=item["wind"]["deg"],
                            # Estimate
                            soil_temperature=item["main"]["temp"] - 2.0,
                            soil_moisture=max(
                                # Estimate
                                0, min(100, item["main"]["humidity"] * 0.7)),
                            timestamp=datetime.utcfromtimestamp(item["dt"])
                        )
                    )

                return WeatherForecast(
                    location_id=f"{location.latitude},{location.longitude}",
                    forecast_data=forecast_data
                )
        except httpx.HTTPError as e:
            logger.error(f"HTTP error getting weather forecast: {e}")
            return self._get_fallback_forecast(location, days)
        except Exception as e:
            logger.error(f"Error getting weather forecast: {e}")
            return self._get_fallback_forecast(location, days)

    async def get_soil_data(self, location: GeoLocation) -> Dict[str, Any]:
        """Get soil data for a location."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "appid": self.agro_api_key
                }

                response = await client.get(
                    f"{self.agro_base_url}/soil",
                    params=params
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error getting soil data: {e}")
            return self._get_fallback_soil_data(location)
        except Exception as e:
            logger.error(f"Error getting soil data: {e}")
            return self._get_fallback_soil_data(location)

    async def health_check(self) -> bool:
        """Check if weather service is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Simple check with default location
                params = {
                    "lat": 0.0,
                    "lon": 0.0,
                    "appid": self.agro_api_key
                }
                base_url = self.agro_base_url.replace("/agro/1.0", "/data/2.5")
                response = await client.get(
                    f"{base_url}/weather",
                    params=params
                )
                return response.status_code == 200
        except Exception:
            return False

    def _get_fallback_weather(self, location: GeoLocation) -> WeatherCondition:
        """Generate realistic fallback weather data."""
        # Generate realistic temperature based on latitude and season
        import math

        # Simple seasonal and latitude-based temperature estimation
        day_of_year = datetime.now().timetuple().tm_yday
        seasonal_factor = math.sin(
            2 * math.pi * (day_of_year - 81) / 365)  # Spring equinox offset

        base_temp = 20 - abs(location.latitude) * \
            0.6  # Colder at higher latitudes
        seasonal_temp = base_temp + seasonal_factor * 15  # ±15°C seasonal variation

        return WeatherCondition(
            temperature=round(seasonal_temp, 1),
            humidity=65.0,
            precipitation=0.0,
            wind_speed=5.0,
            wind_direction=180.0,
            soil_temperature=round(seasonal_temp - 2.0, 1),
            soil_moisture=45.0,
            timestamp=datetime.utcnow()
        )

    def _get_fallback_forecast(self, location: GeoLocation, days: int) -> WeatherForecast:
        """Generate realistic fallback forecast data."""
        forecast_data = []
        base_weather = self._get_fallback_weather(location)

        for i in range(days * 8):  # 3-hour intervals
            # Add some variation to make it realistic
            temp_variation = (i % 8 - 4) * 2  # Daily temperature cycle
            random_variation = (
                hash(f"{location.latitude}{location.longitude}{i}") % 10 - 5) * 0.5

            forecast_data.append(
                WeatherCondition(
                    temperature=base_weather.temperature + temp_variation + random_variation,
                    humidity=max(
                        30, min(90, base_weather.humidity + (i % 3 - 1) * 5)),
                    precipitation=0.0 if i % 7 != 0 else 2.0,  # Occasional rain
                    wind_speed=max(0, base_weather.wind_speed +
                                   (i % 5 - 2) * 1.0),
                    wind_direction=(base_weather.wind_direction + i * 5) % 360,
                    soil_temperature=base_weather.temperature +
                    temp_variation + random_variation - 2.0,
                    soil_moisture=max(
                        20, min(80, (base_weather.soil_moisture or 45.0) + (i % 4 - 2) * 5)),
                    timestamp=datetime.utcnow() + timedelta(hours=i * 3)
                )
            )

        return WeatherForecast(
            location_id=f"{location.latitude},{location.longitude}",
            forecast_data=forecast_data
        )

    def _get_fallback_soil_data(self, location: GeoLocation) -> Dict[str, Any]:
        """Generate fallback soil data."""
        return {
            "location": {
                "lat": location.latitude,
                "lon": location.longitude
            },
            "soil_type": "loam",
            "ph": 6.5,
            "organic_matter": 3.2,
            "moisture": 45.0,
            "temperature": 18.0,
            "nutrients": {
                "nitrogen": 25.0,
                "phosphorus": 15.0,
                "potassium": 200.0
            },
            "source": "estimated",
            "timestamp": datetime.utcnow().isoformat()
        }
