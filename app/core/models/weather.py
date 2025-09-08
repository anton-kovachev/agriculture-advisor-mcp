from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class WeatherCondition(BaseModel):
    """Current or historical weather condition data."""
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

    class Config:
        schema_extra = {
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


class WeatherForecast(BaseModel):
    """Weather forecast data for a specific location."""
    location_id: str = Field(..., description="Reference to the location")
    forecast_data: List[WeatherCondition] = Field(
        ..., description="List of forecasted weather conditions")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Forecast creation timestamp")

    class Config:
        schema_extra = {
            "example": {
                "location_id": "loc_123",
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
