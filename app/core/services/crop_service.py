from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from app.core.models.crop import CropType, GrowthStage, CropInfo
from app.core.models.location import GeoLocation
from app.core.models.weather import WeatherCondition
from .weather_service import WeatherService


class CropManagementService:
    """Service for managing crop-related operations and recommendations."""

    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service
        self._crop_growth_periods = {
            CropType.CORN: {
                GrowthStage.GERMINATION: (5, 7),      # 5-7 days
                GrowthStage.EMERGENCE: (7, 10),       # 7-10 days
                GrowthStage.TILLERING: (20, 30),      # 20-30 days
                GrowthStage.STEM_ELONGATION: (15, 20),  # 15-20 days
                GrowthStage.HEADING: (15, 20),        # 15-20 days
                GrowthStage.FLOWERING: (10, 15),      # 10-15 days
                GrowthStage.GRAIN_FILLING: (35, 45),  # 35-45 days
                GrowthStage.MATURITY: (20, 25),       # 20-25 days
            },
            # Add similar periods for other crop types
        }

        self._optimal_conditions = {
            CropType.CORN: {
                "temperature": (20.0, 30.0),
                "soil_moisture": (50.0, 70.0),
                "soil_ph": (6.0, 7.0)
            },
            CropType.WHEAT: {
                "temperature": (15.0, 25.0),
                "soil_moisture": (40.0, 60.0),
                "soil_ph": (6.0, 7.0)
            },
            CropType.SUNFLOWER: {
                "temperature": (18.0, 28.0),
                "soil_moisture": (45.0, 65.0),
                "soil_ph": (6.0, 7.5)
            }
        }

    async def get_optimal_planting_schedule(
        self,
        crop_type: CropType,
        location: GeoLocation,
        target_harvest_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Calculate the optimal planting schedule based on crop type, location, and target harvest date.
        """
        # Get weather forecast for the next week
        forecast = await self.weather_service.get_weather_forecast(location)

        # If no target harvest date is provided, calculate based on optimal growing season
        if not target_harvest_date:
            # Default to typical growing season length
            growing_days = sum(
                max(period) for period in self._crop_growth_periods[crop_type].values())
            target_harvest_date = datetime.utcnow() + timedelta(days=growing_days)

        # Calculate total growing period needed
        total_days = sum(max(period)
                         for period in self._crop_growth_periods[crop_type].values())

        # Calculate optimal planting date
        optimal_planting_date = target_harvest_date - \
            timedelta(days=total_days)

        # Get expected growth stages timeline
        growth_timeline = self._calculate_growth_timeline(
            crop_type, optimal_planting_date)

        return {
            "optimal_planting_date": optimal_planting_date,
            "target_harvest_date": target_harvest_date,
            "growth_timeline": growth_timeline,
            "total_growing_days": total_days
        }

    async def analyze_growing_conditions(
        self,
        crop_type: CropType,
        location: GeoLocation,
        current_weather: WeatherCondition
    ) -> Dict[str, Any]:
        """
        Analyze current growing conditions and provide recommendations.
        """
        optimal = self._optimal_conditions[crop_type]

        # Check temperature conditions
        temp_min, temp_max = optimal["temperature"]
        temp_status = "optimal" if temp_min <= current_weather.temperature <= temp_max else \
            "too_cold" if current_weather.temperature < temp_min else "too_hot"

        # Check soil moisture if available
        moisture_status = "unknown"
        if current_weather.soil_moisture is not None:
            moisture_min, moisture_max = optimal["soil_moisture"]
            moisture_status = "optimal" if moisture_min <= current_weather.soil_moisture <= moisture_max else \
                "too_dry" if current_weather.soil_moisture < moisture_min else "too_wet"

        # Generate recommendations
        recommendations = []
        if temp_status != "optimal":
            recommendations.append(
                f"Temperature is {temp_status}. Consider protective measures."
            )
        if moisture_status != "optimal" and moisture_status != "unknown":
            recommendations.append(
                f"Soil moisture is {moisture_status}. Adjust irrigation accordingly."
            )

        return {
            "temperature_status": temp_status,
            "moisture_status": moisture_status,
            "recommendations": recommendations,
            "optimal_conditions": optimal
        }

    def _calculate_growth_timeline(
        self,
        crop_type: CropType,
        start_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Calculate the expected timeline for each growth stage.
        """
        timeline = []
        current_date = start_date

        for stage, (min_days, max_days) in self._crop_growth_periods[crop_type].items():
            avg_days = (min_days + max_days) // 2
            stage_end = current_date + timedelta(days=avg_days)

            timeline.append({
                "stage": stage,
                "start_date": current_date,
                "end_date": stage_end,
                "duration_days": avg_days
            })

            current_date = stage_end

        return timeline
