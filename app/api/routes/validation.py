from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from app.core.schemas.advanced_validation import (
    CropManagementQuery,
    SoilAnalysisQuery,
    PestControlQuery,
    IrrigationScheduleQuery,
    HarvestTimingQuery
)

router = APIRouter(
    prefix="/validate",
    tags=["validation"],
    responses={400: {"description": "Invalid input"},
               404: {"description": "Not found"}}
)


@router.post("/crop-management")
async def validate_crop_management(query: CropManagementQuery) -> Dict[str, Any]:
    """Validate crop management parameters and provide recommendations."""
    return {
        "status": "valid",
        "recommendations": [
            "Based on your soil type and climate zone, your crop selection is appropriate.",
            f"Optimal planting window confirmed for {query.crop_type}",
            "Consider soil preparation 2-3 weeks before planting date"
        ]
    }


@router.post("/soil-analysis")
async def validate_soil_analysis(query: SoilAnalysisQuery) -> Dict[str, Any]:
    """Validate soil analysis results and provide recommendations."""
    recommendations = []

    if query.ph_level < 6.0:
        recommendations.append("Consider lime application to raise soil pH")
    elif query.ph_level > 7.5:
        recommendations.append("Consider sulfur application to lower soil pH")

    if query.organic_matter < 3.0:
        recommendations.append(
            "Add organic matter through cover crops or compost")

    return {
        "status": "valid",
        "recommendations": recommendations
    }


@router.post("/pest-control")
async def validate_pest_control(query: PestControlQuery) -> Dict[str, Any]:
    """Validate pest control parameters and provide recommendations."""
    level_info = query.infestation_level

    treatment_urgency = "low" if level_info["level"] <= 2 else \
        "medium" if level_info["level"] == 3 else "high"

    return {
        "status": "valid",
        "urgency": treatment_urgency,
        "description": level_info["description"],
        "recommendations": [
            f"Current infestation level: {level_info['description']}",
            "Consider integrated pest management approach",
            f"Treatment urgency: {treatment_urgency.upper()}"
        ]
    }


@router.post("/irrigation-schedule")
async def validate_irrigation_schedule(query: IrrigationScheduleQuery) -> Dict[str, Any]:
    """Validate irrigation parameters and provide schedule recommendations."""
    return {
        "status": "valid",
        "urgency": query.urgency,
        "recommendations": [
            f"Current soil moisture: {query.soil_moisture}%",
            f"Expected rainfall: {query.expected_rainfall}mm",
            "Adjust irrigation based on weather forecast and soil moisture levels"
        ]
    }


@router.post("/harvest-timing")
async def validate_harvest_timing(query: HarvestTimingQuery) -> Dict[str, Any]:
    """Validate harvest timing parameters and provide recommendations."""
    try:
        # This will trigger the validation
        query.validate_harvest_timing()

        recommendations = ["Conditions are suitable for harvest"]
        if query.grain_moisture:
            recommendations.append(
                f"Grain moisture at {query.grain_moisture}% is within acceptable range")
        if query.rainfall_forecast > 0:
            recommendations.append(
                f"Note: {query.rainfall_forecast}mm rainfall forecasted - plan accordingly")

        return {
            "status": "valid",
            "recommendations": recommendations
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
