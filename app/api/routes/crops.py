from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from datetime import datetime

from app.core.models.crop import CropType, GrowthStage, CropInfo
from app.core.models.location import GeoLocation
from app.core.services import CropManagementService, WeatherService
from app.core.services.crop_service import get_crop_service
from app.core.services.weather_service import get_weather_service

router = APIRouter(
    prefix="/crops",
    tags=["crops"],
    responses={404: {"description": "Not found"}},
)


@router.get("/schedule/{crop_type}/{location_id}")
async def get_planting_schedule(
    crop_type: CropType,
    location_id: str,
    target_harvest_date: datetime | None = None,
    crop_service: CropManagementService = Depends(get_crop_service),
    weather_service: WeatherService = Depends(get_weather_service)
):
    """Get optimal planting schedule for a specific crop and location."""
    try:
        lat, lon = map(float, location_id.split(','))
        location = GeoLocation(latitude=lat, longitude=lon)
        return await crop_service.get_optimal_planting_schedule(
            crop_type, location, target_harvest_date
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conditions/{crop_type}/{location_id}")
async def analyze_conditions(
    crop_type: CropType,
    location_id: str,
    crop_service: CropManagementService = Depends(get_crop_service),
    weather_service: WeatherService = Depends(get_weather_service)
):
    """Analyze growing conditions for a specific crop and location."""
    try:
        lat, lon = map(float, location_id.split(','))
        location = GeoLocation(latitude=lat, longitude=lon)

        # Get current weather conditions first
        current_weather = await weather_service.get_current_weather(location)

        # Analyze conditions based on current weather
        return await crop_service.analyze_growing_conditions(
            crop_type, location, current_weather
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid location format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
