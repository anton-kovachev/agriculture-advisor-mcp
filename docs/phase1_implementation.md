# Phase 1 Implementation: Basic FastMCP Setup

This document provides the initial implementation steps for Phase 1 of the FastMCP migration.

## Prerequisites

1. Install FastMCP:

```bash
uv pip install fastmcp
# or
pip install fastmcp
```

2. Verify installation:

```bash
fastmcp version
```

## Step 1: Create Basic FastMCP Server

Create `src/mcp_server.py`:

```python
from fastmcp import FastMCP
from typing import Dict, Any
import asyncio

# Initialize FastMCP server
mcp = FastMCP(
    name="Agriculture MCP",
    version="2.0.0",
    description="Expert agricultural guidance for corn, wheat, and sunflower cultivation"
)

# Basic test tool
@mcp.tool
async def test_connection() -> str:
    """Test tool to verify MCP server is working"""
    return "Agriculture MCP server is running successfully!"

if __name__ == "__main__":
    # Run with stdio transport (for MCP clients)
    mcp.run()
```

## Step 2: Test Basic Server

Run the server:

```bash
python src/mcp_server.py
```

Test with FastMCP CLI:

```bash
fastmcp run src/mcp_server.py:mcp --transport http --port 8000
```

## Step 3: Create First Agricultural Tool

Add to `src/mcp_server.py`:

```python
from datetime import datetime
from typing import Literal

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
        "next_steps": [
            "Test soil temperature and pH levels",
            "Prepare field with appropriate amendments",
            "Monitor weather forecast for planting window",
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
```

## Step 4: Test the Agricultural Tool

Create a test client `test_client.py`:

```python
import asyncio
from fastmcp import Client

async def test_agriculture_mcp():
    # Connect to HTTP server
    client = Client("http://localhost:8000")

    async with client:
        # Test the crop planting advice tool
        result = await client.call_tool(
            "get_crop_planting_advice",
            {
                "crop_type": "corn",
                "soil_type": "loam",
                "latitude": 41.8781,
                "longitude": -93.0977,
                "planting_season": "spring"
            }
        )

        print("Crop Planting Advice:")
        print(f"Crop: {result['crop_type']}")
        print(f"Location: {result['location']}")
        print(f"Soil Type: {result['soil_type']}")
        print("\nRecommendations:")
        for key, value in result['recommendations'].items():
            print(f"  {key}: {value}")
        print("\nNext Steps:")
        for step in result['next_steps']:
            print(f"  - {step}")

if __name__ == "__main__":
    asyncio.run(test_agriculture_mcp())
```

## Step 5: Run and Test

1. Start the server:

```bash
fastmcp run src/mcp_server.py:mcp --transport http --port 8000
```

2. In another terminal, run the test:

```bash
python test_client.py
```

## Step 6: Add Weather Resource

Add to `src/mcp_server.py`:

```python
@mcp.resource("weather://current/{latitude}/{longitude}")
async def current_weather_resource(latitude: float, longitude: float) -> str:
    """
    Provides current weather conditions for the specified location.
    This is a placeholder that will be connected to real weather APIs.
    """
    # This will be replaced with actual weather service integration
    return f"""
Current Weather for {latitude}, {longitude}:
- Temperature: 22°C
- Humidity: 65%
- Wind Speed: 12 km/h
- Precipitation: 0mm
- Conditions: Partly cloudy

Note: This is placeholder data. Real weather integration coming in Phase 4.
"""

@mcp.resource("crop-calendar://planting/{crop_type}/{latitude}/{longitude}")
async def planting_calendar_resource(
    crop_type: Literal["corn", "wheat", "sunflower"],
    latitude: float,
    longitude: float
) -> str:
    """
    Provides optimal planting calendar for the specified crop and location.
    """
    calendars = {
        "corn": "Optimal planting: Late April to mid-May (when soil reaches 10°C)",
        "wheat": "Winter wheat: September-October, Spring wheat: March-April",
        "sunflower": "Optimal planting: Late April to early June"
    }

    return f"""
Planting Calendar for {crop_type} at {latitude}, {longitude}:

{calendars[crop_type]}

General guidelines:
- Monitor soil temperature daily
- Check 7-day weather forecast
- Ensure no frost risk for 2 weeks
- Verify seed bed preparation
"""
```

## Step 7: Add Farming Prompt Template

Add to `src/mcp_server.py`:

```python
@mcp.prompt("farming-advisor")
async def farming_advisor_prompt(
    crop_type: Literal["corn", "wheat", "sunflower"],
    location: str,
    growth_stage: str = "planning"
) -> str:
    """
    Provides a comprehensive farming advisor prompt template.
    """
    return f"""
You are an expert agricultural advisor specializing in {crop_type} cultivation.

Location: {location}
Current Growth Stage: {growth_stage}

Your expertise includes:
- Soil science and management
- Crop physiology and growth requirements
- Integrated pest management (IPM)
- Precision agriculture techniques
- Sustainable farming practices
- Climate-smart agriculture
- Resource optimization

Provide detailed, actionable advice considering:
1. Local climate and weather patterns
2. Soil conditions and requirements
3. Seasonal timing and growth stages
4. Pest and disease prevention/management
5. Water management and irrigation
6. Nutrient management and fertilization
7. Harvest timing and storage
8. Economic and environmental sustainability

Base all recommendations on:
- Scientific agricultural research
- Local extension service guidelines
- Integrated farming system approaches
- Risk management principles
- Long-term sustainability goals

Always consider the farmer's specific situation, resources, and objectives.
Provide reasoning for each recommendation and include any relevant warnings or cautions.
"""
```

## Next Steps for Phase 2

Once Phase 1 is working:

1. **Environment Setup**: Migrate configuration system from `app/config.py`
2. **Data Models**: Migrate Pydantic models from `app/core/models/`
3. **Weather Integration**: Connect real weather APIs from `app/core/services/weather_service.py`
4. **Advanced Tools**: Implement soil analysis, pest control, irrigation, and harvest timing tools

## Success Criteria for Phase 1

- [ ] FastMCP server starts without errors
- [ ] Basic crop planting advice tool works
- [ ] Weather resource returns data (placeholder)
- [ ] Farming advisor prompt generates useful templates
- [ ] Test client can connect and call tools
- [ ] Server runs with both stdio and HTTP transports

This completes Phase 1 - basic FastMCP server with initial agricultural functionality.
