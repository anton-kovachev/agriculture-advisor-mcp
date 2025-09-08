from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from app.core.models.crop import CropType, GrowthStage


class LocationQuery(BaseModel):
    """Validation model for location-based queries."""
    latitude: float = Field(..., ge=-90, le=90,
                            description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180,
                             description="Longitude in decimal degrees")

    @validator('latitude')
    def validate_latitude(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Latitude must be a number')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Longitude must be a number')
        return v


class WeatherQuery(LocationQuery):
    """Validation model for weather-related queries."""
    start_date: Optional[datetime] = Field(
        None, description="Start date for historical data")
    end_date: Optional[datetime] = Field(
        None, description="End date for historical data")

    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and values['start_date'] and v:
            if v < values['start_date']:
                raise ValueError('End date must be after start date')
        return v


class CropScheduleQuery(LocationQuery):
    """Validation model for crop scheduling queries."""
    crop_type: CropType
    target_harvest_date: Optional[datetime] = Field(
        None, description="Target harvest date")

    @validator('target_harvest_date')
    def validate_harvest_date(cls, v):
        if v and v < datetime.now():
            raise ValueError('Target harvest date must be in the future')
        return v


class ProtectionMeasuresQuery(BaseModel):
    """Validation model for protection measures queries."""
    crop_type: CropType
    growth_stage: GrowthStage
    temperature: float = Field(...,
                               description="Current temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100,
                            description="Current relative humidity percentage")

    @validator('temperature')
    def validate_temperature(cls, v):
        if v < -50 or v > 60:  # Reasonable range for agriculture
            raise ValueError('Temperature must be between -50°C and 60°C')
        return v


class FarmingTechniquesQuery(BaseModel):
    """Validation model for farming techniques queries."""
    crop_type: CropType
    climate_zone: str = Field(..., description="Köppen climate classification")
    soil_type: str = Field(..., description="Primary soil type classification")

    @validator('climate_zone')
    def validate_climate_zone(cls, v):
        valid_zones = [
            'mediterranean', 'continental', 'tropical',
            'semi_arid', 'humid_subtropical'
        ]
        if v.lower() not in valid_zones:
            raise ValueError(
                f'Climate zone must be one of: {", ".join(valid_zones)}')
        return v.lower()
