from typing import Literal, Dict, Any
import json
import logging

from models.location import GeoLocation
from models.weather import WeatherCondition, WeatherForecast
from services.weather_service import WeatherService

logger = logging.getLogger(__name__)


class WeatherTools:
    """Weather-related MCP tools for agricultural planning."""

    def __init__(self):
        self.weather_service = WeatherService()

    async def get_current_weather_conditions(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """
        Get current weather conditions for agricultural planning.

        Args:
            latitude: Latitude in decimal degrees (-90 to 90)
            longitude: Longitude in decimal degrees (-180 to 180)

        Returns:
            Dictionary with current weather data including temperature,
            humidity, precipitation, wind, and soil conditions.
        """
        try:
            location = GeoLocation(latitude=latitude, longitude=longitude)
            weather = await self.weather_service.get_current_weather(location)

            result = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "current_conditions": {
                    "temperature_celsius": weather.temperature,
                    "humidity_percent": weather.humidity,
                    "precipitation_mm": weather.precipitation,
                    "wind_speed_ms": weather.wind_speed,
                    "wind_direction_degrees": weather.wind_direction,
                    "soil_temperature_celsius": weather.soil_temperature,
                    "soil_moisture_percent": weather.soil_moisture,
                    "timestamp": weather.timestamp.isoformat()
                },
                "agricultural_assessment": {
                    "planting_conditions": self._assess_planting_conditions(weather),
                    "irrigation_needed": self._assess_irrigation_need(weather),
                    "field_work_suitable": self._assess_field_work_conditions(weather)
                }
            }

            return result

        except Exception as e:
            logger.error(f"Error getting current weather: {e}")
            return {"error": f"Failed to get weather data: {str(e)}"}

    async def get_weather_forecast_analysis(
        self,
        latitude: float,
        longitude: float,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Get weather forecast with agricultural analysis.

        Args:
            latitude: Latitude in decimal degrees (-90 to 90)
            longitude: Longitude in decimal degrees (-180 to 180)
            days: Number of forecast days (1-7)

        Returns:
            Dictionary with weather forecast and agricultural recommendations.
        """
        try:
            location = GeoLocation(latitude=latitude, longitude=longitude)
            forecast = await self.weather_service.get_weather_forecast(location, days)

            # Analyze forecast for agricultural insights
            analysis = self._analyze_forecast_for_agriculture(
                forecast.forecast_data)

            result = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "forecast": {
                    "days": days,
                    "data": [
                        {
                            "timestamp": condition.timestamp.isoformat(),
                            "temperature_celsius": condition.temperature,
                            "humidity_percent": condition.humidity,
                            "precipitation_mm": condition.precipitation,
                            "wind_speed_ms": condition.wind_speed,
                            "soil_temperature_celsius": condition.soil_temperature,
                            "soil_moisture_percent": condition.soil_moisture
                        }
                        for condition in forecast.forecast_data
                    ]
                },
                "agricultural_analysis": analysis
            }

            return result

        except Exception as e:
            logger.error(f"Error getting weather forecast: {e}")
            return {"error": f"Failed to get forecast data: {str(e)}"}

    async def get_soil_conditions(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """
        Get soil temperature and moisture conditions for planting decisions.

        Args:
            latitude: Latitude in decimal degrees (-90 to 90)
            longitude: Longitude in decimal degrees (-180 to 180)

        Returns:
            Dictionary with soil conditions and planting recommendations.
        """
        try:
            location = GeoLocation(latitude=latitude, longitude=longitude)
            soil_data = await self.weather_service.get_soil_data(location)

            result = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "soil_conditions": {
                    "temperature_celsius": soil_data.get("temperature"),
                    "moisture_percent": soil_data.get("moisture"),
                    "timestamp": soil_data.get("timestamp", "").isoformat() if soil_data.get("timestamp") else None
                },
                "planting_assessment": {
                    "temperature_suitable": self._assess_soil_temperature(soil_data.get("temperature", 0)),
                    "moisture_suitable": self._assess_soil_moisture(soil_data.get("moisture", 0)),
                    "overall_conditions": self._assess_overall_soil_conditions(soil_data)
                }
            }

            return result

        except Exception as e:
            logger.error(f"Error getting soil conditions: {e}")
            return {"error": f"Failed to get soil data: {str(e)}"}

    def _assess_planting_conditions(self, weather: WeatherCondition) -> str:
        """Assess if conditions are suitable for planting."""
        if weather.temperature < 10:
            return "Too cold for most crops"
        elif weather.temperature > 35:
            return "Too hot for optimal planting"
        elif weather.precipitation > 10:
            return "Too wet for planting"
        elif weather.soil_moisture and weather.soil_moisture < 30:
            return "Soil too dry, consider irrigation before planting"
        else:
            return "Good conditions for planting"

    def _assess_irrigation_need(self, weather: WeatherCondition) -> str:
        """Assess irrigation needs based on weather."""
        if weather.soil_moisture and weather.soil_moisture < 40:
            return "Irrigation recommended"
        elif weather.precipitation > 5:
            return "No irrigation needed - recent precipitation"
        else:
            return "Monitor soil moisture"

    def _assess_field_work_conditions(self, weather: WeatherCondition) -> str:
        """Assess if conditions are suitable for field work."""
        if weather.precipitation > 2:
            return "Not suitable - wet conditions"
        elif weather.wind_speed > 15:
            return "Caution - high winds"
        else:
            return "Suitable for field work"

    def _assess_soil_temperature(self, temperature: float) -> str:
        """Assess soil temperature for planting."""
        if temperature < 5:
            return "Too cold for most crops"
        elif temperature < 10:
            return "Cool - suitable for cool season crops only"
        elif temperature < 15:
            return "Moderate - good for many crops"
        elif temperature < 25:
            return "Warm - excellent for most crops"
        else:
            return "Hot - monitor for heat stress"

    def _assess_soil_moisture(self, moisture: float) -> str:
        """Assess soil moisture for planting."""
        if moisture < 20:
            return "Too dry - irrigation needed"
        elif moisture < 40:
            return "Low - consider irrigation"
        elif moisture < 70:
            return "Good - suitable for planting"
        elif moisture < 85:
            return "High - monitor for excess moisture"
        else:
            return "Waterlogged - wait for better drainage"

    def _assess_overall_soil_conditions(self, soil_data: Dict[str, Any]) -> str:
        """Assess overall soil conditions for farming operations."""
        temp = soil_data.get("temperature", 0)
        moisture = soil_data.get("moisture", 0)

        if temp < 10 or moisture < 30:
            return "Wait for better conditions"
        elif temp > 25 and moisture > 80:
            return "Monitor for heat and moisture stress"
        else:
            return "Good conditions for farming operations"

    def _analyze_forecast_for_agriculture(self, forecast_data: list) -> Dict[str, Any]:
        """Analyze weather forecast for agricultural insights."""
        if not forecast_data:
            return {"error": "No forecast data available"}

        # Calculate summary statistics
        total_precipitation = sum(
            condition.precipitation for condition in forecast_data)
        avg_temperature = sum(
            condition.temperature for condition in forecast_data) / len(forecast_data)
        avg_humidity = sum(
            condition.humidity for condition in forecast_data) / len(forecast_data)

        # Identify optimal field work days
        good_work_days = [
            condition for condition in forecast_data
            if condition.precipitation < 2 and condition.wind_speed < 15
        ]

        return {
            "summary": {
                "total_precipitation_mm": round(total_precipitation, 1),
                "average_temperature_celsius": round(avg_temperature, 1),
                "average_humidity_percent": round(avg_humidity, 1),
                "optimal_work_days": len(good_work_days)
            },
            "recommendations": {
                "irrigation_priority": "Low" if total_precipitation > 15 else "High",
                "field_work_windows": f"{len(good_work_days)} days suitable",
                "planting_advice": self._get_planting_forecast_advice(forecast_data),
                "pest_disease_risk": self._assess_pest_disease_risk(avg_temperature, avg_humidity, total_precipitation)
            }
        }

    def _get_planting_forecast_advice(self, forecast_data: list) -> str:
        """Get planting advice based on forecast."""
        suitable_days = [
            condition for condition in forecast_data
            if 10 <= condition.temperature <= 30 and condition.precipitation < 5
        ]

        if len(suitable_days) >= 3:
            return "Good planting window identified"
        elif len(suitable_days) >= 1:
            return "Limited planting opportunities"
        else:
            return "Wait for better conditions"

    def _assess_pest_disease_risk(self, avg_temp: float, avg_humidity: float, total_precip: float) -> str:
        """Assess pest and disease risk based on weather conditions."""
        if avg_humidity > 80 and total_precip > 20:
            return "High - wet conditions favor disease development"
        elif avg_temp > 25 and avg_humidity < 50:
            return "Moderate - warm, dry conditions may increase pest activity"
        else:
            return "Low to moderate - monitor field conditions"
