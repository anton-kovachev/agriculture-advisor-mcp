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
