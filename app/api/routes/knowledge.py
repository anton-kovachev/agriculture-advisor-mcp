from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from datetime import datetime

from app.core.models.crop import CropType, GrowthStage
from app.core.models.location import GeoLocation
from app.core.services import KnowledgeBaseService
from app.core.services.knowledge_service import get_knowledge_service

router = APIRouter(
    prefix="/knowledge",
    tags=["knowledge"],
    responses={404: {"description": "Not found"}},
)


@router.get("/farming-techniques/{crop_type}")
async def get_farming_techniques(
    crop_type: CropType,
    climate_zone: str,
    soil_type: str,
    knowledge_service: KnowledgeBaseService = Depends(get_knowledge_service)
):
    """Get recommended farming techniques for specific conditions."""
    try:
        return knowledge_service.get_farming_techniques(
            crop_type, climate_zone, soil_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/disease-risks/{crop_type}")
async def get_disease_risks(
    crop_type: CropType,
    temperature: float,
    humidity: float,
    knowledge_service: KnowledgeBaseService = Depends(get_knowledge_service)
):
    """Get potential disease risks based on current conditions."""
    try:
        return knowledge_service.get_disease_risks(
            crop_type, temperature, humidity
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/protection-measures/{crop_type}")
async def get_protection_measures(
    crop_type: CropType,
    growth_stage: GrowthStage,
    knowledge_service: KnowledgeBaseService = Depends(get_knowledge_service)
):
    """Get recommended protection measures based on crop type and growth stage."""
    try:
        conditions = {
            "growth_stage": growth_stage,
            # Add any additional condition parameters here
        }
        return knowledge_service.get_protection_measures(
            crop_type, growth_stage, conditions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
