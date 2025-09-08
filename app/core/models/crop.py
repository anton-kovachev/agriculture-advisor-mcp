from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


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
    crop_type: CropType
    growth_stage: GrowthStage
    planting_date: datetime
    expected_harvest_date: datetime
    optimal_temp_range: tuple[float, float] = Field(
        ..., description="Optimal temperature range (min, max) in Celsius")
    optimal_soil_moisture: tuple[float, float] = Field(
        ..., description="Optimal soil moisture range (min, max) in percentage")
    optimal_soil_ph: tuple[float, float] = Field(
        ..., description="Optimal soil pH range (min, max)")

    class Config:
        schema_extra = {
            "example": {
                "crop_type": "corn",
                "growth_stage": "emergence",
                "planting_date": "2025-04-15T00:00:00Z",
                "expected_harvest_date": "2025-09-15T00:00:00Z",
                "optimal_temp_range": (20.0, 30.0),
                "optimal_soil_moisture": (50.0, 70.0),
                "optimal_soil_ph": (6.0, 7.0)
            }
        }
