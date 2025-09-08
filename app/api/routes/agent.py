from fastapi import APIRouter, Depends
from typing import List

from app.core.agent.interface import (
    MCPAgentInterface,
    AgentContext,
    AgentResponse,
    CropManagementQuery,
    SoilAnalysisQuery,
    PestControlQuery,
    IrrigationScheduleQuery,
    HarvestTimingQuery
)

router = APIRouter(prefix="/agent", tags=["agent"])
agent_interface = MCPAgentInterface()

@router.post("/initialize", response_model=AgentResponse)
async def initialize_agent_context(context: AgentContext):
    """Initialize the agent context with location and task information."""
    return await agent_interface.initialize_context(context)

@router.post("/crop-management", response_model=AgentResponse)
async def process_crop_management(
    query: CropManagementQuery,
    context: AgentContext
):
    """Process crop management decisions through the AI agent."""
    return await agent_interface.process_crop_management(query, context)

@router.post("/soil-analysis", response_model=AgentResponse)
async def process_soil_analysis(
    query: SoilAnalysisQuery,
    context: AgentContext
):
    """Process soil analysis data through the AI agent."""
    return await agent_interface.process_soil_analysis(query, context)

@router.post("/pest-control", response_model=AgentResponse)
async def process_pest_control(
    query: PestControlQuery,
    context: AgentContext
):
    """Process pest control situations through the AI agent."""
    return await agent_interface.process_pest_control(query, context)

@router.post("/irrigation-schedule", response_model=AgentResponse)
async def process_irrigation_schedule(
    query: IrrigationScheduleQuery,
    context: AgentContext
):
    """Process irrigation scheduling through the AI agent."""
    return await agent_interface.process_irrigation_schedule(query, context)

@router.post("/harvest-timing", response_model=AgentResponse)
async def process_harvest_timing(
    query: HarvestTimingQuery,
    context: AgentContext
):
    """Process harvest timing decisions through the AI agent."""
    return await agent_interface.process_harvest_timing(query, context)

@router.get("/recommendations", response_model=List[str])
async def get_recommendations(context: AgentContext):
    """Get AI agent recommendations based on current context."""
    return await agent_interface.get_agent_recommendations(context)
