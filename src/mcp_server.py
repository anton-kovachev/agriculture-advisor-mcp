import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Literal

from config import settings
from fastmcp import FastMCP

# Import Phase 2 components
from models.location import GeoLocation
from models.weather import WeatherCondition, WeatherForecast
from models.crop import CropType, GrowthStage, CropInfo
from models.schedule import FarmingActivity, FarmingSchedule
from services.weather_service import WeatherService
from tools.weather_tools import WeatherTools
from resources.weather_resources import WeatherResources

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    name=settings.MCP_SERVER_NAME
)

# Initialize Phase 2 services
weather_service = WeatherService()
weather_tools = WeatherTools()
weather_resources = WeatherResources()

# Mock data storage (in a real implementation, this would be a database)
farms_data: Dict[str, Dict] = {}
weather_cache: Dict[str, Dict] = {}
crop_schedules: Dict[str, List[Dict]] = {}

# ==================== PHASE 2: WEATHER TOOLS ====================


@mcp.tool
async def get_current_weather_conditions(
    latitude: float,
    longitude: float
) -> Dict[str, Any]:
    """
    Get current weather conditions for agricultural planning.

    Args:
        latitude: Farm latitude coordinate (-90 to 90)
        longitude: Farm longitude coordinate (-180 to 180)

    Returns:
        Current weather data with agricultural assessment
    """
    return await weather_tools.get_current_weather_conditions(latitude, longitude)


@mcp.tool
async def get_weather_forecast_analysis(
    latitude: float,
    longitude: float,
    days: int = 3
) -> Dict[str, Any]:
    """
    Get weather forecast with agricultural analysis.

    Args:
        latitude: Farm latitude coordinate (-90 to 90)
        longitude: Farm longitude coordinate (-180 to 180)
        days: Number of forecast days (1-7)

    Returns:
        Weather forecast with agricultural recommendations
    """
    return await weather_tools.get_weather_forecast_analysis(latitude, longitude, days)


@mcp.tool
async def get_soil_conditions(
    latitude: float,
    longitude: float
) -> Dict[str, Any]:
    """
    Get soil temperature and moisture conditions for planting decisions.

    Args:
        latitude: Farm latitude coordinate (-90 to 90)
        longitude: Farm longitude coordinate (-180 to 180)

    Returns:
        Soil conditions with planting recommendations
    """
    return await weather_tools.get_soil_conditions(latitude, longitude)

# ==================== PHASE 1: EXISTING TOOLS ====================


@mcp.tool
async def test_connection() -> str:
    """Test tool to verify MCP server is working"""
    return "Agriculture MCP server is running successfully with Phase 2 weather integration!"


@mcp.tool
async def get_crop_planting_advice(
    crop_type: Literal["corn", "wheat", "sunflower"],
    soil_type: Literal["clay", "loam", "sandy", "silt"],
    latitude: float,
    longitude: float,
    planting_season: Literal["spring", "summer", "fall"]
) -> Dict[str, Any]:
    """
    Get expert advice on crop planting based on location and conditions.

    Args:
        crop_type: Type of crop to plant (corn, wheat, or sunflower)
        soil_type: Soil classification of the field
        latitude: Farm latitude coordinate (-90 to 90)
        longitude: Farm longitude coordinate (-180 to 180)
        planting_season: Intended planting season

    Returns:
        Comprehensive planting advice including timing and recommendations
    """

    # Basic crop-specific advice
    crop_advice = {
        "corn": {
            "soil_temp_min": 10,  # Celsius
            "planting_depth": "1.5-2 inches",
            "row_spacing": "30-36 inches",
            "optimal_ph": "6.0-6.8"
        },
        "wheat": {
            "soil_temp_min": 4,   # Celsius
            "planting_depth": "1-2 inches",
            "row_spacing": "6-8 inches",
            "optimal_ph": "6.0-7.0"
        },
        "sunflower": {
            "soil_temp_min": 10,  # Celsius
            "planting_depth": "1.5-2.5 inches",
            "row_spacing": "20-30 inches",
            "optimal_ph": "6.0-7.5"
        }
    }

    advice = crop_advice[crop_type]

    # Get current weather conditions for enhanced recommendations
    try:
        current_weather = await weather_tools.get_current_weather_conditions(latitude, longitude)
        weather_assessment = current_weather.get(
            "agricultural_assessment", {}) if isinstance(current_weather, dict) else {}
    except Exception as e:
        logger.warning(f"Could not fetch weather data: {e}")
        weather_assessment = {}

    return {
        "crop_type": crop_type,
        "location": {"latitude": latitude, "longitude": longitude},
        "soil_type": soil_type,
        "season": planting_season,
        "recommendations": {
            "minimum_soil_temperature": f"{advice['soil_temp_min']}°C",
            "planting_depth": advice["planting_depth"],
            "row_spacing": advice["row_spacing"],
            "optimal_soil_ph": advice["optimal_ph"],
            "soil_compatibility": _check_soil_compatibility(crop_type, soil_type),
            "seasonal_notes": _get_seasonal_notes(crop_type, planting_season)
        },
        "current_conditions": weather_assessment,
        "next_steps": [
            "Test soil temperature and pH levels",
            "Check current weather conditions",
            "Monitor 7-day weather forecast",
            "Prepare field with appropriate amendments",
            "Ensure seed quality and treatment"
        ]
    }


def _check_soil_compatibility(crop_type: str, soil_type: str) -> str:
    """Check compatibility between crop and soil type"""
    compatibility = {
        "corn": {
            "clay": "Good - retains moisture and nutrients well",
            "loam": "Excellent - ideal growing medium",
            "sandy": "Fair - may need more irrigation and fertilization",
            "silt": "Good - good drainage and nutrient retention"
        },
        "wheat": {
            "clay": "Good - retains moisture for winter varieties",
            "loam": "Excellent - best overall performance",
            "sandy": "Poor - may need significant amendments",
            "silt": "Very good - excellent water and nutrient retention"
        },
        "sunflower": {
            "clay": "Fair - ensure good drainage to prevent root rot",
            "loam": "Excellent - optimal growing conditions",
            "sandy": "Good - naturally well-draining",
            "silt": "Good - adequate drainage with good nutrients"
        }
    }
    return compatibility[crop_type][soil_type]


def _get_seasonal_notes(crop_type: str, season: str) -> str:
    """Get season-specific planting notes"""
    notes = {
        "corn": {
            "spring": "Plant after last frost when soil reaches 10°C",
            "summer": "Early summer planting possible in northern regions",
            "fall": "Not recommended - insufficient growing season"
        },
        "wheat": {
            "spring": "Plant early spring for spring wheat varieties",
            "summer": "Not typical planting season",
            "fall": "Ideal for winter wheat varieties"
        },
        "sunflower": {
            "spring": "Plant after last frost, soil temperature 10°C+",
            "summer": "Early summer planting possible",
            "fall": "Not recommended - insufficient time to maturity"
        }
    }
    return notes[crop_type][season]

# ==================== PHASE 2: WEATHER RESOURCES ====================


@mcp.resource("weather://current/{latitude}/{longitude}")
async def current_weather_resource(latitude: float, longitude: float) -> str:
    """
    Provides current weather conditions for the specified location with agricultural analysis.
    """
    return await weather_resources.get_current_weather_resource(latitude, longitude)


@mcp.resource("weather://forecast/{latitude}/{longitude}")
async def weather_forecast_resource(latitude: float, longitude: float) -> str:
    """
    Provides weather forecast for agricultural planning.
    """
    return await weather_resources.get_weather_forecast_resource(latitude, longitude, days=3)


@mcp.resource("crop-calendar/{crop_type}/{latitude}/{longitude}")
async def crop_calendar_resource(crop_type: str, latitude: float, longitude: float) -> str:
    """
    Provides crop planting calendar based on location and weather patterns.
    """
    return await weather_resources.get_crop_calendar_resource(crop_type, latitude, longitude)

# ==================== PROMPTS ====================


@mcp.prompt("farming-advisor")
async def farming_advisor_prompt(
    crop_type: Literal["corn", "wheat", "sunflower"],
    location: str,
    growth_stage: str = "planning"
) -> str:
    """
    Provides a comprehensive farming advisor prompt template with weather integration.
    """
    return f"""
You are an expert agricultural advisor specializing in {crop_type} cultivation with access to real-time weather data.

Location: {location}
Current Growth Stage: {growth_stage}

Your expertise includes:
- Soil science and management
- Crop physiology and growth requirements  
- Weather-based decision making
- Integrated pest management (IPM)
- Precision agriculture techniques
- Sustainable farming practices
- Climate-smart agriculture
- Resource optimization

Provide detailed, actionable advice considering:
1. Real-time weather conditions and forecasts
2. Soil temperature and moisture data
3. Local climate and weather patterns
4. Seasonal timing and growth stages
5. Pest and disease prevention/management
6. Water management and irrigation scheduling
7. Nutrient management and fertilization
8. Harvest timing and storage
9. Economic and environmental sustainability

Base all recommendations on:
- Current and forecasted weather data
- Scientific agricultural research
- Local extension service guidelines
- Integrated farming system approaches
- Risk management principles
- Long-term sustainability goals

Always consider the farmer's specific situation, resources, and objectives.
Provide reasoning for each recommendation and include any relevant warnings or cautions.
Use real weather data to inform timing recommendations for planting, spraying, harvesting, and other field operations.
"""


@mcp.prompt("weather-advisor")
async def weather_advisor_prompt(
    latitude: float,
    longitude: float,
    operation_type: str = "general"
) -> str:
    """
    Provides weather-focused agricultural advice prompt.
    """
    return f"""
You are an agricultural meteorologist providing weather-based farming advice for location {latitude}, {longitude}.

Current Analysis Focus: {operation_type}

Your expertise includes:
- Agricultural meteorology and microclimates
- Weather pattern interpretation for farming
- Irrigation scheduling based on weather
- Field operation timing recommendations
- Crop protection from weather extremes
- Seasonal planning with climate data

Provide weather-based recommendations for:
1. Current field operation suitability
2. Short-term planning (next 3-7 days)
3. Irrigation scheduling and water management
4. Pest and disease pressure related to weather
5. Harvest timing and quality considerations
6. Equipment operation safety in current conditions

Always base advice on:
- Current weather conditions
- Detailed weather forecasts
- Soil moisture and temperature data
- Historical weather patterns for the region
- Risk assessment for weather-related crop damage

Consider farmer safety and equipment protection in all weather-related recommendations.
"""

if __name__ == "__main__":
    import sys

    # Check command line arguments for transport type
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        # HTTP transport mode
        port = 8000
        if len(sys.argv) > 2 and sys.argv[2].startswith("--port="):
            port = int(sys.argv[2].split("=")[1])

        print(f"🚀 Starting Agriculture MCP Server on HTTP port {port}")
        print("🌾 Phase 2: Real weather integration enabled")
        mcp.run(transport="http", port=port)
    else:
        # Default STDIO transport
        print("🚀 Starting Agriculture MCP Server with STDIO transport")
        print("🌾 Phase 2: Real weather integration enabled")
        mcp.run()
