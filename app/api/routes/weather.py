from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List, Dict, Any
from datetime import datetime
from functools import lru_cache

from app.core.models.location import GeoLocation
from app.core.models.weather import WeatherCondition, WeatherForecast
from app.core.services.weather_service import WeatherService


@lru_cache()
def get_weather_service():
    return WeatherService()

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/current/{location_id}",
    response_model=WeatherCondition,
    summary="Get Current Weather",
    description="Retrieve current weather conditions for a specific location",
    response_description="Current weather conditions including temperature, humidity, precipitation, and wind data",
    responses={
        200: {
            "description": "Successfully retrieved weather data",
            "content": {
                "application/json": {
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
            }
        },
        400: {"description": "Invalid location format"},
        404: {"description": "Location not found"},
        500: {"description": "Internal server error or weather service unavailable"}
    }
)
async def get_current_weather(
    location_id: str = Path(...,
                            description="Location ID in format 'latitude,longitude'"),
    weather_service: WeatherService = Depends(get_weather_service)
):
    """
    Get current weather conditions for a specific location.

    Parameters:
    - location_id: String in format 'latitude,longitude' (e.g., '45.523064,-122.676483')

    Returns:
    - WeatherCondition object containing current weather data

    Raises:
    - HTTPException(400): If location format is invalid
    - HTTPException(404): If location is not found
    - HTTPException(500): If weather service is unavailable
    """
    try:
        # Parse location_id into lat/lon
        lat, lon = map(float, location_id.split(','))
        location = GeoLocation(latitude=lat, longitude=lon)
        return await weather_service.get_current_weather(location)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast/{location_id}", response_model=WeatherForecast)
async def get_weather_forecast(
    location_id: str,
    days: int = 7,
    weather_service: WeatherService = Depends(get_weather_service)
):
    """Get weather forecast for a specific location."""
    try:
        lat, lon = map(float, location_id.split(','))
        location = GeoLocation(latitude=lat, longitude=lon)
        return await weather_service.get_weather_forecast(location, days)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/soil/{location_id}")
async def get_soil_data(
    location_id: str,
    weather_service: WeatherService = Depends(get_weather_service)
):
    """Get soil data for a specific location."""
    try:
        lat, lon = map(float, location_id.split(','))
        location = GeoLocation(latitude=lat, longitude=lon)
        return await weather_service.get_soil_data(location)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
