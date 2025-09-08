from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .crop import CropType, GrowthStage


class FarmingActivity(BaseModel):
    """Individual farming activity in the schedule."""
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
    crop_type: CropType
    location_id: str = Field(..., description="Reference to the location")
    planting_date: datetime
    expected_harvest_date: datetime
    current_growth_stage: GrowthStage
    activities: List[FarmingActivity] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "crop_type": "corn",
                "location_id": "loc_123",
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
