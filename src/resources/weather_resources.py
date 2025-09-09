import json
from typing import Dict, Any
import logging

from models.location import GeoLocation
from services.weather_service import WeatherService

logger = logging.getLogger(__name__)


class WeatherResources:
    """Weather-related MCP resources for agricultural data access."""

    def __init__(self):
        self.weather_service = WeatherService()

    async def get_current_weather_resource(
        self,
        latitude: float,
        longitude: float
    ) -> str:
        """
        Provides current weather conditions for the specified location.
        Used by agricultural planning tools and recommendations.
        """
        try:
            location = GeoLocation(latitude=latitude, longitude=longitude)
            weather = await self.weather_service.get_current_weather(location)

            return f"""
Current Weather Conditions for {latitude}, {longitude}:

🌡️  Temperature: {weather.temperature}°C
💧  Humidity: {weather.humidity}%
🌧️  Precipitation: {weather.precipitation}mm
💨  Wind: {weather.wind_speed} m/s from {weather.wind_direction}°
🌱  Soil Temperature: {weather.soil_temperature or 'N/A'}°C
🪣  Soil Moisture: {weather.soil_moisture or 'N/A'}%
📅  Updated: {weather.timestamp.strftime('%Y-%m-%d %H:%M UTC')}

Agricultural Assessment:
- Planting Conditions: {_assess_planting_conditions(weather)}
- Irrigation Status: {_assess_irrigation_need(weather)}
- Field Work: {_assess_field_work_conditions(weather)}
"""
        except Exception as e:
            logger.error(f"Error getting weather resource: {e}")
            return f"Error retrieving weather data: {str(e)}"

    async def get_weather_forecast_resource(
        self,
        latitude: float,
        longitude: float,
        days: int = 3
    ) -> str:
        """
        Provides weather forecast for agricultural planning.
        """
        try:
            location = GeoLocation(latitude=latitude, longitude=longitude)
            forecast = await self.weather_service.get_weather_forecast(location, days)

            result = f"Weather Forecast for {latitude}, {longitude} ({days} days):\n\n"

            # Group by day and show daily summary
            daily_data = {}
            for condition in forecast.forecast_data:
                date_key = condition.timestamp.date()
                if date_key not in daily_data:
                    daily_data[date_key] = []
                daily_data[date_key].append(condition)

            for date, conditions in sorted(daily_data.items()):
                avg_temp = sum(
                    c.temperature for c in conditions) / len(conditions)
                total_precip = sum(c.precipitation for c in conditions)
                avg_humidity = sum(
                    c.humidity for c in conditions) / len(conditions)

                result += f"""📅 {date.strftime('%Y-%m-%d')}:
   🌡️  Avg Temperature: {avg_temp:.1f}°C
   🌧️  Total Precipitation: {total_precip:.1f}mm
   💧  Avg Humidity: {avg_humidity:.1f}%
   
"""

            # Add agricultural recommendations
            total_rain = sum(c.precipitation for c in forecast.forecast_data)
            result += f"""
🚜 Agricultural Outlook:
- Total Expected Rainfall: {total_rain:.1f}mm
- Irrigation Needs: {'Low' if total_rain > 15 else 'Moderate to High'}
- Field Work Windows: Check individual days for dry periods
- Planting Conditions: Monitor daily temperatures and moisture
"""

            return result

        except Exception as e:
            logger.error(f"Error getting forecast resource: {e}")
            return f"Error retrieving forecast data: {str(e)}"

    async def get_crop_calendar_resource(
        self,
        crop_type: str,
        latitude: float,
        longitude: float
    ) -> str:
        """
        Provides crop planting calendar based on location and weather patterns.
        """
        try:
            # Get current weather to assess conditions
            location = GeoLocation(latitude=latitude, longitude=longitude)
            current_weather = await self.weather_service.get_current_weather(location)

            # Crop-specific recommendations (this would be expanded with real data)
            crop_info = {
                "corn": {
                    "optimal_temp_range": "20-30°C",
                    "planting_season": "Spring (April-June)",
                    "soil_temp_requirement": "10°C+",
                    "growing_days": "90-120 days"
                },
                "wheat": {
                    "optimal_temp_range": "15-25°C",
                    "planting_season": "Fall (September-November) or Spring (March-May)",
                    "soil_temp_requirement": "4°C+",
                    "growing_days": "120-150 days"
                },
                "sunflower": {
                    "optimal_temp_range": "20-28°C",
                    "planting_season": "Late Spring (May-June)",
                    "soil_temp_requirement": "12°C+",
                    "growing_days": "80-120 days"
                }
            }

            info = crop_info.get(crop_type.lower(), crop_info["corn"])

            return f"""
🌾 Crop Calendar for {crop_type.title()} at {latitude}, {longitude}:

📋 Crop Information:
- Optimal Temperature: {info['optimal_temp_range']}
- Planting Season: {info['planting_season']}
- Soil Temperature Needed: {info['soil_temp_requirement']}
- Growing Period: {info['growing_days']}

🌡️ Current Conditions:
- Air Temperature: {current_weather.temperature}°C
- Soil Temperature: {current_weather.soil_temperature or 'N/A'}°C
- Soil Moisture: {current_weather.soil_moisture or 'N/A'}%

📅 Planting Recommendation:
{_get_planting_recommendation(crop_type, current_weather)}

🔔 Next Steps:
1. Monitor soil temperature trends
2. Check 7-day weather forecast
3. Prepare soil if conditions are favorable
4. Plan irrigation schedule based on precipitation forecast
"""

        except Exception as e:
            logger.error(f"Error getting crop calendar resource: {e}")
            return f"Error retrieving crop calendar: {str(e)}"


# Helper functions (reused from tools)
def _assess_planting_conditions(weather) -> str:
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


def _assess_irrigation_need(weather) -> str:
    """Assess irrigation needs based on weather."""
    if weather.soil_moisture and weather.soil_moisture < 40:
        return "Irrigation recommended"
    elif weather.precipitation > 5:
        return "No irrigation needed - recent precipitation"
    else:
        return "Monitor soil moisture"


def _assess_field_work_conditions(weather) -> str:
    """Assess if conditions are suitable for field work."""
    if weather.precipitation > 2:
        return "Not suitable - wet conditions"
    elif weather.wind_speed > 15:
        return "Caution - high winds"
    else:
        return "Suitable for field work"


def _get_planting_recommendation(crop_type: str, weather) -> str:
    """Get planting recommendation for specific crop."""
    temp = weather.temperature
    soil_temp = weather.soil_temperature or temp - 2

    if crop_type.lower() == "corn":
        if soil_temp < 10:
            return "Wait - soil temperature too low for corn planting"
        elif temp > 30:
            return "Consider waiting for cooler weather"
        else:
            return "Good conditions for corn planting"
    elif crop_type.lower() == "wheat":
        if soil_temp < 4:
            return "Wait - soil temperature too low for wheat"
        elif 15 <= temp <= 25:
            return "Excellent conditions for wheat planting"
        else:
            return "Acceptable conditions for wheat planting"
    elif crop_type.lower() == "sunflower":
        if soil_temp < 12:
            return "Wait - soil temperature too low for sunflowers"
        elif 20 <= temp <= 28:
            return "Ideal conditions for sunflower planting"
        else:
            return "Acceptable conditions for sunflower planting"
    else:
        return "Monitor temperature and soil conditions for optimal planting"
