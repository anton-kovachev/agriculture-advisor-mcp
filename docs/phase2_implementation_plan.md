# Phase 2 Implementation Plan: Weather Services and Data Models Migration

## Overview

Phase 2 focuses on migrating the existing FastAPI weather services and data models to the FastMCP framework. This phase will establish the core data infrastructure needed for agricultural decision-making tools, integrating real weather APIs and creating a robust foundation for advanced farming features.

## Objectives

- ✅ **Migrate Pydantic Models**: Adapt existing data models to FastMCP-compatible structure
- ✅ **Weather Service Integration**: Port weather service functionality from FastAPI to FastMCP
- ✅ **API Compatibility**: Ensure seamless integration with existing external weather APIs
- ✅ **Resource Implementation**: Replace placeholder weather resources with real data
- ✅ **Testing Infrastructure**: Comprehensive testing for weather services and data models

## Pre-Implementation Assessment

### Current State Analysis

#### Existing FastAPI Structure

```
app/
├── core/
│   ├── models/
│   │   ├── location.py       # GeoLocation model
│   │   ├── weather.py        # WeatherCondition, WeatherForecast
│   │   ├── crop.py          # CropType, GrowthStage, CropInfo
│   │   ├── schedule.py      # FarmingActivity, FarmingSchedule
│   │   └── __init__.py      # Model exports
│   ├── services/
│   │   └── weather_service.py  # WeatherService class
│   └── schemas/
│       └── validation.py    # Request/response validation
└── api/
    └── routes/
        └── weather.py       # FastAPI weather endpoints
```

#### Target FastMCP Structure

```
src/
├── models/
│   ├── location.py          # Migrated GeoLocation
│   ├── weather.py           # Migrated weather models
│   ├── crop.py             # Migrated crop models
│   ├── schedule.py         # Migrated schedule models
│   └── __init__.py         # Model exports
├── services/
│   └── weather_service.py  # FastMCP-compatible WeatherService
├── tools/
│   └── weather_tools.py    # Weather-related MCP tools
└── resources/
    └── weather_resources.py # Weather MCP resources
```

## Implementation Steps

### Step 1: Data Models Migration

#### 1.1 Create Models Directory Structure

```bash
mkdir -p src/models
```

#### 1.2 Migrate Location Model

**File**: `src/models/location.py`

```python
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GeoLocation(BaseModel):
    """Geographic location model with coordinates and basic geographical information."""
    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "latitude": 45.523064,
                "longitude": -122.676483,
                "elevation": 15.2,
                "climate_zone": "Csb",
                "soil_type": "Clay loam"
            }
        }
    )

    latitude: float = Field(..., ge=-90, le=90,
                            description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180,
                             description="Longitude in decimal degrees")
    elevation: Optional[float] = Field(
        default=None, description="Elevation in meters above sea level")
    climate_zone: Optional[str] = Field(
        default=None, description="Köppen climate classification")
    soil_type: Optional[str] = Field(
        default=None, description="Primary soil type classification")
```

#### 1.3 Migrate Weather Models

**File**: `src/models/weather.py`

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class WeatherCondition(BaseModel):
    """Current or historical weather condition data."""
    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "temperature": 22.5,
                "humidity": 65.0,
                "precipitation": 0.0,
                "wind_speed": 3.5,
                "wind_direction": 180.0,
                "soil_temperature": 18.2,
                "soil_moisture": 45.0,
                "timestamp": "2025-09-07T12:00:00Z"
            }
        }
    )

    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100,
                            description="Relative humidity percentage")
    precipitation: float = Field(..., ge=0, description="Precipitation in mm")
    wind_speed: float = Field(..., ge=0, description="Wind speed in m/s")
    wind_direction: float = Field(..., ge=0, le=360,
                                  description="Wind direction in degrees")
    soil_temperature: Optional[float] = Field(
        None, description="Soil temperature in Celsius")
    soil_moisture: Optional[float] = Field(
        None, ge=0, le=100, description="Soil moisture percentage")
    timestamp: datetime = Field(...,
                                description="Timestamp of the weather data")


class WeatherForecast(BaseModel):
    """Weather forecast data for a specific location."""
    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "location_id": "45.523064,-122.676483",
                "forecast_data": [{
                    "temperature": 24.5,
                    "humidity": 62.0,
                    "precipitation": 0.0,
                    "wind_speed": 4.2,
                    "wind_direction": 195.0,
                    "soil_temperature": 20.1,
                    "soil_moisture": 42.0,
                    "timestamp": "2025-09-08T12:00:00Z"
                }],
                "created_at": "2025-09-07T12:00:00Z"
            }
        }
    )

    location_id: str = Field(..., description="Reference to the location")
    forecast_data: List[WeatherCondition] = Field(
        ..., description="List of forecasted weather conditions")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Forecast creation timestamp")
```

#### 1.4 Migrate Crop Models

**File**: `src/models/crop.py`

```python
from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field, ConfigDict


class CropType(str, Enum):
    """Supported crop types."""
    CORN = "corn"
    SUNFLOWER = "sunflower"
    WHEAT = "wheat"


class GrowthStage(str, Enum):
    """Generic growth stages for cereal crops."""
    GERMINATION = "germination"
    EMERGENCE = "emergence"
    TILLERING = "tillering"
    STEM_ELONGATION = "stem_elongation"
    HEADING = "heading"
    FLOWERING = "flowering"
    GRAIN_FILLING = "grain_filling"
    MATURITY = "maturity"


class CropInfo(BaseModel):
    """Detailed information about a specific crop type."""
    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "crop_type": "corn",
                "growth_stage": "emergence",
                "planting_date": "2025-04-15T00:00:00Z",
                "expected_harvest_date": "2025-09-15T00:00:00Z",
                "optimal_temp_range": [20.0, 30.0],
                "optimal_soil_moisture": [50.0, 70.0],
                "optimal_soil_ph": [6.0, 7.0]
            }
        }
    )

    crop_type: CropType
    growth_stage: GrowthStage
    planting_date: datetime
    expected_harvest_date: datetime
    optimal_temp_range: Tuple[float, float] = Field(
        ..., description="Optimal temperature range (min, max) in Celsius")
    optimal_soil_moisture: Tuple[float, float] = Field(
        ..., description="Optimal soil moisture range (min, max) in percentage")
    optimal_soil_ph: Tuple[float, float] = Field(
        ..., description="Optimal soil pH range (min, max)")
```

#### 1.5 Migrate Schedule Models

**File**: `src/models/schedule.py`

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from .crop import CropType, GrowthStage


class FarmingActivity(BaseModel):
    """Individual farming activity in the schedule."""
    model_config = ConfigDict(extra="ignore")

    activity_type: str = Field(..., description="Type of farming activity")
    description: str = Field(...,
                             description="Detailed description of the activity")
    scheduled_date: datetime = Field(...,
                                     description="Planned date for the activity")
    completed_date: Optional[datetime] = Field(
        None, description="Actual completion date")
    notes: Optional[str] = Field(
        None, description="Additional notes or observations")


class FarmingSchedule(BaseModel):
    """Complete farming schedule for a specific crop and location."""
    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "crop_type": "corn",
                "location_id": "45.523064,-122.676483",
                "planting_date": "2025-04-15T00:00:00Z",
                "expected_harvest_date": "2025-09-15T00:00:00Z",
                "current_growth_stage": "emergence",
                "activities": [
                    {
                        "activity_type": "soil_preparation",
                        "description": "Prepare soil with initial fertilization",
                        "scheduled_date": "2025-04-10T00:00:00Z",
                        "completed_date": "2025-04-10T00:00:00Z",
                        "notes": "Soil pH adjusted to 6.5"
                    }
                ],
                "last_updated": "2025-09-07T12:00:00Z"
            }
        }
    )

    crop_type: CropType
    location_id: str = Field(..., description="Reference to the location")
    planting_date: datetime
    expected_harvest_date: datetime
    current_growth_stage: GrowthStage
    activities: List[FarmingActivity] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
```

#### 1.6 Create Models Module Init

**File**: `src/models/__init__.py`

```python
from .location import GeoLocation
from .weather import WeatherCondition, WeatherForecast
from .crop import CropType, GrowthStage, CropInfo
from .schedule import FarmingActivity, FarmingSchedule

__all__ = [
    'GeoLocation',
    'WeatherCondition',
    'WeatherForecast',
    'CropType',
    'GrowthStage',
    'CropInfo',
    'FarmingActivity',
    'FarmingSchedule',
]
```

### Step 2: Weather Service Migration

#### 2.1 Create Services Directory

```bash
mkdir -p src/services
```

#### 2.2 Migrate Weather Service

**File**: `src/services/weather_service.py`

```python
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import httpx
import logging

from src.models.weather import WeatherCondition, WeatherForecast
from src.models.location import GeoLocation
from src.config import settings

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for retrieving weather data from external APIs."""

    def __init__(self):
        self.agro_api_key = settings.AGROMONITORING_API_KEY
        self.weather_api_key = settings.WEATHER_COMPANY_API_KEY
        self.agro_base_url = settings.AGROMONITORING_BASE_URL
        self.weather_base_url = settings.WEATHER_COMPANY_BASE_URL
        self.timeout = 30.0

    async def get_current_weather(self, location: GeoLocation) -> WeatherCondition:
        """Get current weather conditions for a location."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "appid": self.agro_api_key,
                    "units": "metric"
                }

                response = await client.get(
                    f"{self.agro_base_url}/weather",
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
                    soil_temperature=data.get("main", {}).get("temp", 0.0) - 2.0,  # Estimate
                    soil_moisture=data["main"]["humidity"] * 0.7,  # Estimate
                    timestamp=datetime.utcfromtimestamp(data["dt"])
                )
        except httpx.HTTPError as e:
            logger.error(f"HTTP error getting current weather: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting current weather: {e}")
            raise

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
                    "cnt": min(days * 8, 40),  # 3-hour forecasts, max 40 (5 days)
                    "units": "metric"
                }

                response = await client.get(
                    f"{self.agro_base_url}/forecast",
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
                            soil_temperature=item["main"]["temp"] - 2.0,  # Estimate
                            soil_moisture=item["main"]["humidity"] * 0.7,  # Estimate
                            timestamp=datetime.utcfromtimestamp(item["dt"])
                        )
                    )

                return WeatherForecast(
                    location_id=f"{location.latitude},{location.longitude}",
                    forecast_data=forecast_data
                )
        except httpx.HTTPError as e:
            logger.error(f"HTTP error getting weather forecast: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting weather forecast: {e}")
            raise

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
            raise
        except Exception as e:
            logger.error(f"Error getting soil data: {e}")
            raise

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
                response = await client.get(
                    f"{self.agro_base_url}/weather",
                    params=params
                )
                return response.status_code == 200
        except Exception:
            return False
```

### Step 3: Weather Tools Implementation

#### 3.1 Create Weather Tools

**File**: `src/tools/weather_tools.py`

```python
from typing import Literal, Dict, Any
import json
import logging

from src.models.location import GeoLocation
from src.models.weather import WeatherCondition, WeatherForecast
from src.services.weather_service import WeatherService

logger = logging.getLogger(__name__)


class WeatherTools:
    """Weather-related MCP tools for agricultural planning."""

    def __init__(self):
        self.weather_service = WeatherService()

    async def get_current_weather_conditions(
        self,
        latitude: float,
        longitude: float
    ) -> str:
        """
        Get current weather conditions for agricultural planning.

        Args:
            latitude: Latitude in decimal degrees (-90 to 90)
            longitude: Longitude in decimal degrees (-180 to 180)

        Returns:
            JSON string with current weather data including temperature,
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
                "agricultural_insights": {
                    "planting_conditions": _assess_planting_conditions(weather),
                    "irrigation_needed": _assess_irrigation_need(weather),
                    "field_work_suitable": _assess_field_work_conditions(weather)
                }
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.error(f"Error getting current weather: {e}")
            return json.dumps({"error": f"Failed to get weather data: {str(e)}"})

    async def get_weather_forecast_analysis(
        self,
        latitude: float,
        longitude: float,
        days: int = 7
    ) -> str:
        """
        Get weather forecast with agricultural analysis.

        Args:
            latitude: Latitude in decimal degrees (-90 to 90)
            longitude: Longitude in decimal degrees (-180 to 180)
            days: Number of forecast days (1-7)

        Returns:
            JSON string with weather forecast and agricultural recommendations.
        """
        try:
            location = GeoLocation(latitude=latitude, longitude=longitude)
            forecast = await self.weather_service.get_weather_forecast(location, days)

            # Analyze forecast for agricultural insights
            analysis = _analyze_forecast_for_agriculture(forecast.forecast_data)

            result = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "forecast_period": {
                    "days": days,
                    "created_at": forecast.created_at.isoformat()
                },
                "daily_forecasts": [
                    {
                        "date": condition.timestamp.date().isoformat(),
                        "temperature": condition.temperature,
                        "humidity": condition.humidity,
                        "precipitation": condition.precipitation,
                        "wind_speed": condition.wind_speed,
                        "soil_moisture": condition.soil_moisture
                    }
                    for condition in forecast.forecast_data[::8]  # Daily samples
                ],
                "agricultural_analysis": analysis
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.error(f"Error getting weather forecast: {e}")
            return json.dumps({"error": f"Failed to get forecast data: {str(e)}"})

    async def get_soil_conditions(
        self,
        latitude: float,
        longitude: float
    ) -> str:
        """
        Get detailed soil conditions for the specified location.

        Args:
            latitude: Latitude in decimal degrees (-90 to 90)
            longitude: Longitude in decimal degrees (-180 to 180)

        Returns:
            JSON string with soil data and agricultural recommendations.
        """
        try:
            location = GeoLocation(latitude=latitude, longitude=longitude)
            soil_data = await self.weather_service.get_soil_data(location)

            result = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "soil_conditions": soil_data,
                "recommendations": _generate_soil_recommendations(soil_data)
            }

            return json.dumps(result, indent=2)

        except Exception as e:
            logger.error(f"Error getting soil data: {e}")
            return json.dumps({"error": f"Failed to get soil data: {str(e)}"})


# Helper functions for agricultural analysis
def _assess_planting_conditions(weather: WeatherCondition) -> str:
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


def _assess_irrigation_need(weather: WeatherCondition) -> str:
    """Assess irrigation needs based on weather."""
    if weather.soil_moisture and weather.soil_moisture < 40:
        return "Irrigation recommended"
    elif weather.precipitation > 5:
        return "No irrigation needed - recent precipitation"
    else:
        return "Monitor soil moisture"


def _assess_field_work_conditions(weather: WeatherCondition) -> str:
    """Assess if conditions are suitable for field work."""
    if weather.precipitation > 2:
        return "Not suitable - wet conditions"
    elif weather.wind_speed > 15:
        return "Caution - high winds"
    else:
        return "Suitable for field work"


def _analyze_forecast_for_agriculture(forecast_data: list) -> Dict[str, Any]:
    """Analyze weather forecast for agricultural planning."""
    total_precipitation = sum(f.precipitation for f in forecast_data)
    avg_temperature = sum(f.temperature for f in forecast_data) / len(forecast_data)
    avg_humidity = sum(f.humidity for f in forecast_data) / len(forecast_data)

    return {
        "total_precipitation_mm": round(total_precipitation, 1),
        "average_temperature_celsius": round(avg_temperature, 1),
        "average_humidity_percent": round(avg_humidity, 1),
        "irrigation_recommendation": (
            "Minimal irrigation needed" if total_precipitation > 20
            else "Regular irrigation recommended"
        ),
        "optimal_planting_days": [
            f.timestamp.date().isoformat()
            for f in forecast_data
            if 15 <= f.temperature <= 30 and f.precipitation < 5
        ][:3]  # Top 3 days
    }


def _generate_soil_recommendations(soil_data: Dict[str, Any]) -> Dict[str, str]:
    """Generate soil management recommendations."""
    # This would be expanded based on actual soil data structure
    return {
        "general": "Monitor soil conditions regularly",
        "moisture": "Maintain adequate soil moisture for crop growth",
        "temperature": "Soil temperature affects seed germination and root development"
    }
```

### Step 4: Weather Resources Implementation

#### 4.1 Create Weather Resources

**File**: `src/resources/weather_resources.py`

```python
import json
from typing import Dict, Any
import logging

from src.models.location import GeoLocation
from src.services.weather_service import WeatherService

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
                avg_temp = sum(c.temperature for c in conditions) / len(conditions)
                total_precip = sum(c.precipitation for c in conditions)
                avg_humidity = sum(c.humidity for c in conditions) / len(conditions)

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
```

### Step 5: Integration with Main Server

#### 5.1 Update Main Server File

**File**: `src/mcp_server.py` (additions)

```python
# Add these imports at the top
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastmcp import FastMCP
from typing import Literal
import logging

# Import migrated components
from models.location import GeoLocation
from models.weather import WeatherCondition, WeatherForecast
from models.crop import CropType, GrowthStage, CropInfo
from services.weather_service import WeatherService
from tools.weather_tools import WeatherTools
from resources.weather_resources import WeatherResources
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Agriculture MCP")

# Initialize services
weather_service = WeatherService()
weather_tools = WeatherTools()
weather_resources = WeatherResources()

# Add new weather tools
@mcp.tool()
async def get_current_weather_conditions(
    latitude: float,
    longitude: float
) -> str:
    """
    Get current weather conditions for agricultural planning.

    Args:
        latitude: Latitude in decimal degrees (-90 to 90)
        longitude: Longitude in decimal degrees (-180 to 180)
    """
    return await weather_tools.get_current_weather_conditions(latitude, longitude)

@mcp.tool()
async def get_weather_forecast_analysis(
    latitude: float,
    longitude: float,
    days: int = 7
) -> str:
    """
    Get weather forecast with agricultural analysis.

    Args:
        latitude: Latitude in decimal degrees (-90 to 90)
        longitude: Longitude in decimal degrees (-180 to 180)
        days: Number of forecast days (1-7)
    """
    return await weather_tools.get_weather_forecast_analysis(latitude, longitude, days)

@mcp.tool()
async def get_soil_conditions(
    latitude: float,
    longitude: float
) -> str:
    """
    Get detailed soil conditions for the specified location.

    Args:
        latitude: Latitude in decimal degrees (-90 to 90)
        longitude: Longitude in decimal degrees (-180 to 180)
    """
    return await weather_tools.get_soil_conditions(latitude, longitude)

# Update existing weather resource to use real data
@mcp.resource("weather://current/{latitude}/{longitude}")
async def current_weather_resource(latitude: float, longitude: float) -> str:
    """
    Provides current weather conditions for the specified location.
    Now connected to real weather APIs for accurate agricultural planning.
    """
    return await weather_resources.get_current_weather_resource(latitude, longitude)

# Add new weather resources
@mcp.resource("weather://forecast/{latitude}/{longitude}/{days}")
async def weather_forecast_resource(
    latitude: float,
    longitude: float,
    days: int = 3
) -> str:
    """
    Provides weather forecast for agricultural planning.
    """
    return await weather_resources.get_weather_forecast_resource(latitude, longitude, days)

# Update existing crop calendar resource
@mcp.resource("crop-calendar://planting/{crop_type}/{latitude}/{longitude}")
async def planting_calendar_resource(
    crop_type: Literal["corn", "wheat", "sunflower"],
    latitude: float,
    longitude: float
) -> str:
    """
    Provides crop planting calendar based on location and weather patterns.
    Now includes real weather data for accurate recommendations.
    """
    return await weather_resources.get_crop_calendar_resource(crop_type, latitude, longitude)

# Add health check tool
@mcp.tool()
async def check_weather_service_health() -> str:
    """
    Check if weather service APIs are available and responding.
    """
    try:
        is_healthy = await weather_service.health_check()
        status = "✅ Available" if is_healthy else "❌ Unavailable"
        return f"Weather Service Status: {status}"
    except Exception as e:
        return f"Weather Service Status: ❌ Error - {str(e)}"

# Rest of the existing server code...
```

### Step 6: Configuration Updates

#### 6.1 Update Configuration

**File**: `src/config.py` (additions)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Existing settings...
    WEATHER_COMPANY_API_KEY: str = ""
    WEATHER_COMPANY_BASE_URL: str = "https://api.weather.com/v1"
    AGROMONITORING_API_KEY: str = ""
    AGROMONITORING_BASE_URL: str = "https://api.agromonitoring.com/agro/1.0"

    # Weather service configuration
    WEATHER_TIMEOUT: int = 30
    WEATHER_CACHE_TTL: int = 300  # 5 minutes

    # Agricultural thresholds
    MIN_PLANTING_TEMP: float = 10.0
    MAX_PLANTING_TEMP: float = 35.0
    MIN_SOIL_MOISTURE: float = 30.0
    IRRIGATION_THRESHOLD: float = 40.0

settings = Settings()
```

### Step 7: Testing Infrastructure

#### 7.1 Create Weather Service Tests

**File**: `tests/test_weather_service.py`

```python
import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from src.models.location import GeoLocation
from src.models.weather import WeatherCondition
from src.services.weather_service import WeatherService


@pytest.fixture
def weather_service():
    return WeatherService()


@pytest.fixture
def test_location():
    return GeoLocation(latitude=45.523064, longitude=-122.676483)


@pytest.fixture
def mock_weather_response():
    return {
        "main": {"temp": 22.5, "humidity": 65},
        "wind": {"speed": 3.5, "deg": 180},
        "rain": {"1h": 0.0},
        "dt": 1725724800  # Example timestamp
    }


class TestWeatherService:
    @pytest.mark.asyncio
    async def test_get_current_weather_success(
        self,
        weather_service,
        test_location,
        mock_weather_response
    ):
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_weather_response
            mock_response.raise_for_status.return_value = None

            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            result = await weather_service.get_current_weather(test_location)

            assert isinstance(result, WeatherCondition)
            assert result.temperature == 22.5
            assert result.humidity == 65
            assert result.wind_speed == 3.5

    @pytest.mark.asyncio
    async def test_get_current_weather_api_error(self, weather_service, test_location):
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("API Error")

            with pytest.raises(Exception, match="API Error"):
                await weather_service.get_current_weather(test_location)

    @pytest.mark.asyncio
    async def test_health_check_success(self, weather_service):
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            result = await weather_service.health_check()
            assert result is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self, weather_service):
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception()

            result = await weather_service.health_check()
            assert result is False
```

#### 7.2 Create Integration Tests

**File**: `tests/test_phase2_integration.py`

```python
import pytest
import json
from unittest.mock import AsyncMock, patch

from src.tools.weather_tools import WeatherTools
from src.resources.weather_resources import WeatherResources


@pytest.fixture
def weather_tools():
    return WeatherTools()


@pytest.fixture
def weather_resources():
    return WeatherResources()


class TestPhase2Integration:
    @pytest.mark.asyncio
    async def test_weather_tools_integration(self, weather_tools):
        """Test that weather tools return properly formatted responses."""
        with patch.object(weather_tools.weather_service, 'get_current_weather') as mock_weather:
            mock_weather.return_value = AsyncMock(
                temperature=22.5,
                humidity=65.0,
                precipitation=0.0,
                wind_speed=3.5,
                wind_direction=180.0,
                soil_temperature=18.2,
                soil_moisture=45.0,
                timestamp=datetime.now()
            )

            result = await weather_tools.get_current_weather_conditions(45.5, -122.7)

            # Verify result is valid JSON
            data = json.loads(result)
            assert "location" in data
            assert "current_conditions" in data
            assert "agricultural_insights" in data
            assert data["current_conditions"]["temperature_celsius"] == 22.5

    @pytest.mark.asyncio
    async def test_weather_resources_integration(self, weather_resources):
        """Test that weather resources return formatted text responses."""
        with patch.object(weather_resources.weather_service, 'get_current_weather') as mock_weather:
            mock_weather.return_value = AsyncMock(
                temperature=22.5,
                humidity=65.0,
                precipitation=0.0,
                wind_speed=3.5,
                wind_direction=180.0,
                soil_temperature=18.2,
                soil_moisture=45.0,
                timestamp=datetime.now()
            )

            result = await weather_resources.get_current_weather_resource(45.5, -122.7)

            # Verify result contains expected sections
            assert "Current Weather Conditions" in result
            assert "Temperature:" in result
            assert "Agricultural Assessment:" in result
            assert "22.5°C" in result

    def test_models_pydantic_v2_compatibility(self):
        """Test that migrated models work with Pydantic v2."""
        from src.models.location import GeoLocation
        from src.models.weather import WeatherCondition
        from src.models.crop import CropInfo, CropType, GrowthStage

        # Test GeoLocation
        location = GeoLocation(latitude=45.5, longitude=-122.7)
        assert location.latitude == 45.5
        assert location.longitude == -122.7

        # Test WeatherCondition
        weather = WeatherCondition(
            temperature=22.5,
            humidity=65.0,
            precipitation=0.0,
            wind_speed=3.5,
            wind_direction=180.0,
            timestamp=datetime.now()
        )
        assert weather.temperature == 22.5

        # Test CropInfo
        crop = CropInfo(
            crop_type=CropType.CORN,
            growth_stage=GrowthStage.EMERGENCE,
            planting_date=datetime.now(),
            expected_harvest_date=datetime.now(),
            optimal_temp_range=(20.0, 30.0),
            optimal_soil_moisture=(50.0, 70.0),
            optimal_soil_ph=(6.0, 7.0)
        )
        assert crop.crop_type == CropType.CORN
```

### Step 8: Documentation Updates

#### 8.1 Update Dependencies

**File**: `requirements-fastmcp.txt` (additions)

```txt
# Add to existing requirements
httpx>=0.25.0
pytest-asyncio>=0.21.0
```

## Success Criteria

- [ ] **Model Migration**: All Pydantic models migrated to FastMCP-compatible structure
- [ ] **Service Integration**: Weather service successfully integrated with real API calls
- [ ] **Tool Implementation**: Weather tools provide JSON responses with agricultural insights
- [ ] **Resource Implementation**: Weather resources provide formatted text with recommendations
- [ ] **Error Handling**: Robust error handling for API failures and network issues
- [ ] **Testing**: Comprehensive test suite with >90% coverage
- [ ] **Documentation**: Clear documentation for new weather features
- [ ] **Performance**: API responses within 5 seconds under normal conditions

## Risk Mitigation

1. **API Rate Limits**: Implement caching and request throttling
2. **Network Failures**: Graceful fallbacks to cached data or offline recommendations
3. **Data Quality**: Validation and sanitization of external weather data
4. **Configuration**: Secure API key management and environment-specific settings

## Phase 2 Completion Timeline

- **Week 1**: Models migration and basic service setup
- **Week 2**: Tools and resources implementation
- **Week 3**: Integration testing and error handling
- **Week 4**: Documentation and performance optimization

## Next Phase Preview

**Phase 3** will focus on advanced agricultural features:

- Crop scheduling optimization
- Pest and disease prediction
- Irrigation management
- Harvest timing recommendations
- Integration with farm management systems

This Phase 2 plan provides a comprehensive roadmap for migrating weather services and establishing the data foundation needed for advanced agricultural decision-making tools in the FastMCP framework.
