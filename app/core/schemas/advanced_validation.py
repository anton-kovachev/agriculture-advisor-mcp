from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class SoilType(str, Enum):
    """Soil type classifications."""
    CLAY = "clay"
    CLAY_LOAM = "clay_loam"
    LOAM = "loam"
    SANDY_LOAM = "sandy_loam"
    SANDY = "sandy"
    SILT_LOAM = "silt_loam"
    SILTY_CLAY = "silty_clay"


class ClimateZone(str, Enum):
    """Köppen climate classifications relevant for agriculture."""
    MEDITERRANEAN = "mediterranean"
    CONTINENTAL = "continental"
    TROPICAL = "tropical"
    SEMI_ARID = "semi_arid"
    HUMID_SUBTROPICAL = "humid_subtropical"
    OCEANIC = "oceanic"
    SUBARCTIC = "subarctic"


class IrrigationMethod(str, Enum):
    """Available irrigation methods."""
    DRIP = "drip"
    SPRINKLER = "sprinkler"
    FLOOD = "flood"
    CENTER_PIVOT = "center_pivot"
    SUBSURFACE = "subsurface"


class CropManagementQuery(BaseModel):
    """Base model for crop management queries."""
    crop_type: str
    planting_date: datetime
    field_size: float = Field(..., gt=0, description="Field size in hectares")
    previous_crop: Optional[str] = None
    soil_type: SoilType
    irrigation_method: Optional[IrrigationMethod] = None
    climate_zone: ClimateZone
    expected_rainfall: Optional[float] = Field(None, ge=0)

    @field_validator('planting_date')
    @classmethod
    def validate_planting_date(cls, v):
        if v < datetime.now() - timedelta(days=365):
            raise ValueError(
                "Planting date cannot be more than a year in the past")
        if v > datetime.now() + timedelta(days=365):
            raise ValueError(
                "Planting date cannot be more than a year in the future")
        return v

    @model_validator(mode='after')
    def validate_crop_requirements(self) -> 'CropManagementQuery':
        crop_type = self.crop_type
        soil_type = self.soil_type
        climate_zone = self.climate_zone

        if crop_type == 'wheat':
            if soil_type in [SoilType.SANDY, SoilType.SILTY_CLAY]:
                raise ValueError("Wheat prefers loamy or clay loam soils")
            if climate_zone == ClimateZone.TROPICAL:
                raise ValueError("Wheat is not suitable for tropical climates")

        elif crop_type == 'corn':
            if climate_zone in [ClimateZone.SUBARCTIC, ClimateZone.MEDITERRANEAN]:
                raise ValueError("Corn requires longer growing seasons")
            if not getattr(self, 'irrigation_method', None) and getattr(self, 'expected_rainfall', 0) < 500:
                raise ValueError(
                    "Corn requires either irrigation or sufficient rainfall")

        return self


class SoilAnalysisQuery(BaseModel):
    """Model for soil analysis queries."""
    ph_level: float = Field(..., ge=0, le=14)
    organic_matter: float = Field(..., ge=0, le=100)
    nitrogen: float = Field(..., ge=0)
    phosphorus: float = Field(..., ge=0)
    potassium: float = Field(..., ge=0)
    soil_moisture: float = Field(..., ge=0, le=100)

    @model_validator(mode='after')
    def check_npk_levels(self) -> 'SoilAnalysisQuery':
        """Validate NPK levels are within reasonable ranges."""
        if self.nitrogen > 500:  # Example threshold
            raise ValueError("Nitrogen level seems unreasonably high")
        if self.phosphorus > 300:
            raise ValueError("Phosphorus level seems unreasonably high")
        if self.potassium > 800:
            raise ValueError("Potassium level seems unreasonably high")
        return self


class PestControlQuery(BaseModel):
    """Model for pest control queries."""
    pest_type: str
    infestation_level: int = Field(..., ge=1, le=5)
    crop_stage: str
    temperature: float
    humidity: float
    previous_treatments: List[str] = []

    @field_validator('infestation_level')
    @classmethod
    def validate_infestation(cls, v: int) -> Dict[str, Any]:
        """Validate infestation level description."""
        descriptions = {
            1: "Minor presence - Monitoring required",
            2: "Light infestation - Consider treatment",
            3: "Moderate infestation - Treatment recommended",
            4: "Severe infestation - Immediate treatment required",
            5: "Critical infestation - Emergency measures needed"
        }
        return {"level": v, "description": descriptions[v]}


class IrrigationScheduleQuery(BaseModel):
    """Model for irrigation scheduling queries."""
    crop_type: str
    growth_stage: str
    soil_moisture: float = Field(..., ge=0, le=100)
    expected_rainfall: float = Field(..., ge=0)
    temperature: float
    humidity: float
    wind_speed: float = Field(..., ge=0)
    urgency: str = ""  # Field to store irrigation urgency

    @model_validator(mode='after')
    def check_irrigation_needs(self) -> 'IrrigationScheduleQuery':
        """Validate irrigation parameters and provide recommendations."""
        self.urgency: str = ""  # Add urgency field
        if self.soil_moisture < 30 and self.expected_rainfall < 10:
            if self.temperature > 30 and self.humidity < 50:
                self.urgency = "High - Immediate irrigation needed"
            else:
                self.urgency = "Medium - Monitor conditions"
        else:
            self.urgency = "Low - Adequate moisture"
        return self


class HarvestTimingQuery(BaseModel):
    """Model for harvest timing queries."""
    crop_type: str
    planting_date: datetime
    growing_degree_days: float = Field(..., ge=0)
    grain_moisture: Optional[float] = Field(None, ge=0, le=100)
    rainfall_forecast: float = Field(..., ge=0)

    @model_validator(mode='after')
    def validate_harvest_timing(self) -> 'HarvestTimingQuery':
        """Validate harvest timing parameters."""
        if self.crop_type == 'corn' and self.growing_degree_days < 2700:
            raise ValueError(
                "Insufficient growing degree days for corn harvest")
        if self.grain_moisture and self.crop_type == 'wheat' and self.grain_moisture > 18:
            raise ValueError("Grain moisture too high for wheat harvest")
        return self
