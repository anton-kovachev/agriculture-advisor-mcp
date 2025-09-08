# Agriculture MCP Rewrite Implementation Plan

## Migrating from FastAPI to FastMCP Python Library

### Project Overview

This plan outlines the complete rewrite of the Agriculture MCP project to utilize the FastMCP Python library (https://gofastmcp.com/) instead of the current FastAPI implementation. The migration will transform the project from a REST API to a proper Model Context Protocol (MCP) server.

---

## Phase 1: Project Analysis & Setup

**Duration: 1-2 days**

### 1.1 Current State Assessment

- **Current Architecture**: FastAPI-based REST API with weather services, validation schemas, and agent interfaces
- **Key Components**:
  - Weather service integration (AgroMonitoring API)
  - Advanced validation schemas for crops (corn, wheat, sunflower)
  - Agent interface for AI interactions
  - Route handlers for different agricultural operations
- **Dependencies**: FastAPI, Uvicorn, Pydantic, httpx, python-dotenv

### 1.2 FastMCP Research & Setup

- [x] Research FastMCP 2.0 capabilities and API
- [ ] Install FastMCP library: `pip install fastmcp`
- [ ] Review FastMCP documentation for tools, resources, and prompts
- [ ] Understand MCP protocol differences from REST API

### 1.3 Project Structure Planning

```
agriculture-mcp/
├── src/
│   ├── mcp_server.py              # Main FastMCP server
│   ├── tools/                     # MCP tools (formerly API endpoints)
│   │   ├── __init__.py
│   │   ├── crop_management.py
│   │   ├── soil_analysis.py
│   │   ├── pest_control.py
│   │   ├── irrigation.py
│   │   └── harvest_timing.py
│   ├── resources/                 # MCP resources (data providers)
│   │   ├── __init__.py
│   │   ├── weather_data.py
│   │   ├── soil_data.py
│   │   └── crop_calendar.py
│   ├── prompts/                   # MCP prompts (templates)
│   │   ├── __init__.py
│   │   ├── farming_advisor.py
│   │   └── crop_specific.py
│   ├── core/                      # Core business logic
│   │   ├── models/               # Pydantic models
│   │   ├── services/             # External API services
│   │   └── schemas/              # Validation schemas
│   └── config.py                 # Configuration
├── tests/                        # Test files
├── docs/                         # Documentation
├── requirements.txt              # Dependencies
└── README.md                     # Updated documentation
```

---

## Phase 2: Core Infrastructure Migration

**Duration: 2-3 days**

### 2.1 Environment & Dependencies

- [ ] Update `requirements.txt` with FastMCP dependencies
- [ ] Remove FastAPI, Uvicorn dependencies
- [ ] Add FastMCP: `fastmcp>=2.11.0`
- [ ] Update Python version requirements (FastMCP requires Python 3.8+)

### 2.2 Configuration System

- [ ] Migrate `app/config.py` to new structure
- [ ] Maintain environment variable system for API keys
- [ ] Add FastMCP-specific configuration options

**Implementation:**

```python
# src/config.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Weather API Configuration
    AGROMONITORING_API_KEY: str
    AGROMONITORING_BASE_URL: str = "http://api.agromonitoring.com/agro/1.0"
    WEATHER_COMPANY_API_KEY: Optional[str] = None
    WEATHER_COMPANY_BASE_URL: Optional[str] = None

    # MCP Server Configuration
    MCP_SERVER_NAME: str = "Agriculture MCP"
    MCP_SERVER_VERSION: str = "2.0.0"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2.3 Main MCP Server Setup

- [ ] Create `src/mcp_server.py` as the main server file
- [ ] Initialize FastMCP instance
- [ ] Set up basic server structure

**Implementation:**

```python
# src/mcp_server.py
from fastmcp import FastMCP
from src.config import settings

# Initialize FastMCP server
mcp = FastMCP(
    name=settings.MCP_SERVER_NAME,
    version=settings.MCP_SERVER_VERSION,
    description="Expert agricultural guidance for corn, wheat, and sunflower cultivation"
)

if __name__ == "__main__":
    mcp.run()
```

---

## Phase 3: Data Models Migration

**Duration: 1-2 days**

### 3.1 Pydantic Models Reuse

- [ ] Review existing models in `app/core/models/`
- [ ] Migrate location, weather, and crop models
- [ ] Ensure compatibility with FastMCP tool signatures

### 3.2 Schema Validation Migration

- [ ] Migrate validation schemas from `app/core/schemas/`
- [ ] Adapt for MCP tool input/output validation
- [ ] Maintain type safety and validation rules

**Key Models to Migrate:**

- `GeoLocation`: Geographic coordinates
- `WeatherCondition`: Weather data structure
- `WeatherForecast`: Forecast data
- `CropManagementQuery`: Crop planning inputs
- `SoilAnalysisQuery`: Soil testing parameters
- `PestControlQuery`: Pest management data
- `IrrigationScheduleQuery`: Irrigation planning
- `HarvestTimingQuery`: Harvest timing data

---

## Phase 4: External Services Migration

**Duration: 1-2 days**

### 4.1 Weather Service Migration

- [ ] Migrate `app/core/services/weather_service.py`
- [ ] Maintain AgroMonitoring API integration
- [ ] Adapt for use in MCP resources and tools

### 4.2 Service Integration

- [ ] Ensure async compatibility with FastMCP
- [ ] Maintain error handling and retry logic
- [ ] Add proper logging and monitoring

**Implementation:**

```python
# src/core/services/weather_service.py
import httpx
from typing import Dict, Any
from src.core.models.weather import WeatherCondition, WeatherForecast
from src.core.models.location import GeoLocation
from src.config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.AGROMONITORING_API_KEY
        self.base_url = settings.AGROMONITORING_BASE_URL

    async def get_current_weather(self, location: GeoLocation) -> WeatherCondition:
        # Existing implementation adapted for FastMCP
        pass

    async def get_weather_forecast(self, location: GeoLocation, days: int = 7) -> WeatherForecast:
        # Existing implementation adapted for FastMCP
        pass
```

---

## Phase 5: MCP Tools Implementation

**Duration: 3-4 days**

### 5.1 Crop Management Tools

- [ ] Convert crop management endpoints to MCP tools
- [ ] Implement `@mcp.tool` decorators
- [ ] Maintain existing business logic

**Implementation:**

```python
# src/tools/crop_management.py
from src.mcp_server import mcp
from src.core.schemas.advanced_validation import CropManagementQuery
from src.core.services.weather_service import WeatherService

@mcp.tool
async def get_crop_planting_advice(
    crop_type: str,
    soil_type: str,
    climate_zone: str,
    latitude: float,
    longitude: float,
    planting_season: str
) -> dict:
    """
    Get expert advice on crop planting based on location, soil, and climate conditions.

    Args:
        crop_type: Type of crop (corn, wheat, sunflower)
        soil_type: Soil classification (clay, loam, sandy, etc.)
        climate_zone: Climate zone classification
        latitude: Farm latitude coordinate
        longitude: Farm longitude coordinate
        planting_season: Intended planting season (spring, summer, fall)

    Returns:
        Comprehensive planting advice including timing, preparation, and recommendations
    """
    # Implementation logic here
    pass
```

### 5.2 Soil Analysis Tools

- [ ] Convert soil analysis functionality to MCP tools
- [ ] Implement nutrient analysis and recommendations

### 5.3 Irrigation Management Tools

- [ ] Convert irrigation scheduling to MCP tools
- [ ] Integrate weather data for smart irrigation advice

### 5.4 Pest Control Tools

- [ ] Convert pest management functionality to MCP tools
- [ ] Implement IPM (Integrated Pest Management) recommendations

### 5.5 Harvest Timing Tools

- [ ] Convert harvest timing functionality to MCP tools
- [ ] Integrate weather forecasts and crop maturity indicators

---

## Phase 6: MCP Resources Implementation

**Duration: 2-3 days**

### 6.1 Weather Data Resources

- [ ] Implement weather data as MCP resources
- [ ] Provide real-time weather access to LLMs

**Implementation:**

```python
# src/resources/weather_data.py
from src.mcp_server import mcp
from src.core.services.weather_service import WeatherService

@mcp.resource("weather://current/{latitude}/{longitude}")
async def current_weather(latitude: float, longitude: float) -> str:
    """
    Provides current weather conditions for the specified location.
    """
    # Implementation
    pass

@mcp.resource("weather://forecast/{latitude}/{longitude}/{days}")
async def weather_forecast(latitude: float, longitude: float, days: int = 7) -> str:
    """
    Provides weather forecast for the specified location and duration.
    """
    # Implementation
    pass
```

### 6.2 Crop Calendar Resources

- [ ] Implement seasonal crop calendars as resources
- [ ] Provide planting and harvest timing data

### 6.3 Soil Data Resources

- [ ] Implement soil information as resources
- [ ] Provide soil classification and characteristics

---

## Phase 7: MCP Prompts Implementation

**Duration: 1-2 days**

### 7.1 Farming Advisor Prompts

- [ ] Create reusable prompt templates for agricultural advice
- [ ] Implement crop-specific guidance prompts

**Implementation:**

```python
# src/prompts/farming_advisor.py
from src.mcp_server import mcp

@mcp.prompt("farming-advisor")
async def farming_advisor_prompt(
    crop_type: str,
    location: str,
    growth_stage: str = "planning"
) -> str:
    """
    Provides a comprehensive farming advisor prompt template for the specified crop and location.
    """
    return f"""
    You are an expert agricultural advisor specializing in {crop_type} cultivation.

    Location: {location}
    Growth Stage: {growth_stage}

    Provide detailed, actionable advice considering:
    - Local climate and weather patterns
    - Soil conditions and requirements
    - Seasonal timing and growth stages
    - Integrated pest management
    - Sustainable farming practices
    - Resource optimization

    Base your recommendations on scientific agricultural practices and local conditions.
    """
```

### 7.2 Crop-Specific Prompts

- [ ] Create prompts for corn, wheat, and sunflower
- [ ] Include growth stage-specific guidance

---

## Phase 8: Testing Framework

**Duration: 2-3 days**

### 8.1 Unit Tests

- [ ] Migrate existing tests to FastMCP framework
- [ ] Test individual tools, resources, and prompts
- [ ] Implement FastMCP testing utilities

### 8.2 Integration Tests

- [ ] Test complete farming workflows
- [ ] Test weather API integrations
- [ ] Test MCP protocol compliance

### 8.3 End-to-End Tests

- [ ] Test with actual MCP clients
- [ ] Test Claude integration scenarios
- [ ] Performance and reliability testing

**Implementation:**

```python
# tests/test_tools.py
import pytest
from fastmcp.testing import MCPTest
from src.mcp_server import mcp

@pytest.mark.asyncio
async def test_crop_planting_advice():
    async with MCPTest(mcp) as client:
        result = await client.call_tool(
            "get_crop_planting_advice",
            {
                "crop_type": "corn",
                "soil_type": "loam",
                "climate_zone": "temperate",
                "latitude": 41.8781,
                "longitude": -93.0977,
                "planting_season": "spring"
            }
        )
        assert result["success"] is True
        assert "recommendations" in result
```

---

## Phase 9: Documentation Update

**Duration: 1-2 days**

### 9.1 README Update

- [ ] Update project description for MCP focus
- [ ] Add FastMCP installation instructions
- [ ] Update usage examples

### 9.2 API Documentation

- [ ] Document MCP tools, resources, and prompts
- [ ] Create integration examples
- [ ] Update Claude integration guide

### 9.3 Migration Guide

- [ ] Document changes from FastAPI version
- [ ] Provide migration assistance for users

---

## Phase 10: Deployment & Integration

**Duration: 1-2 days**

### 10.1 Local Development

- [ ] Test local MCP server with stdio transport
- [ ] Verify tool functionality
- [ ] Test resource access

### 10.2 FastMCP Cloud Deployment

- [ ] Deploy to FastMCP Cloud for remote access
- [ ] Configure authentication if needed
- [ ] Test remote MCP access

### 10.3 Claude Integration

- [ ] Update Claude integration examples
- [ ] Test with Claude Desktop and API
- [ ] Verify MCP protocol compliance

---

## Success Criteria

### Technical Requirements

- [x] All existing functionality migrated to MCP tools
- [ ] Weather API integration maintained
- [ ] Comprehensive test coverage (>80%)
- [ ] Documentation complete and accurate
- [ ] Performance equivalent or better than FastAPI version

### Functional Requirements

- [ ] Crop management advice tools working
- [ ] Soil analysis tools functional
- [ ] Irrigation scheduling tools operational
- [ ] Pest control tools working
- [ ] Harvest timing tools functional
- [ ] Weather data resources accessible
- [ ] Prompts generating useful templates

### Integration Requirements

- [ ] Claude Desktop integration working
- [ ] Claude API integration functional
- [ ] FastMCP Cloud deployment successful
- [ ] MCP protocol compliance verified

---

## Risk Assessment & Mitigation

### High-Risk Items

1. **Weather API Integration**: Ensure async compatibility
   - _Mitigation_: Thorough testing with httpx async client
2. **Complex Business Logic**: Maintain accuracy during migration
   - _Mitigation_: Extensive unit and integration testing
3. **MCP Protocol Compliance**: Ensure proper implementation
   - _Mitigation_: Use FastMCP testing utilities and examples

### Medium-Risk Items

1. **Performance**: Ensure FastMCP performs as well as FastAPI
   - _Mitigation_: Performance benchmarking and optimization
2. **Documentation**: Maintain comprehensive documentation
   - _Mitigation_: Progressive documentation updates

### Low-Risk Items

1. **Configuration**: Environment variable migration
   - _Mitigation_: Gradual migration with fallbacks

---

## Dependencies & Prerequisites

### Technical Dependencies

- Python 3.8+ (FastMCP requirement)
- FastMCP library (latest stable version)
- Existing environment variables and API keys
- Git repository for FastMCP Cloud deployment

### Knowledge Requirements

- Understanding of MCP protocol concepts
- FastMCP API familiarity
- Agricultural domain knowledge maintenance
- Testing framework knowledge

---

## Timeline Summary

| Phase               | Duration | Dependencies | Deliverables                         |
| ------------------- | -------- | ------------ | ------------------------------------ |
| 1. Project Analysis | 1-2 days | None         | Analysis document, project structure |
| 2. Infrastructure   | 2-3 days | Phase 1      | Core server setup, configuration     |
| 3. Data Models      | 1-2 days | Phase 2      | Migrated models and schemas          |
| 4. Services         | 1-2 days | Phase 3      | Weather service integration          |
| 5. MCP Tools        | 3-4 days | Phase 4      | All agricultural tools implemented   |
| 6. MCP Resources    | 2-3 days | Phase 5      | Weather and data resources           |
| 7. MCP Prompts      | 1-2 days | Phase 6      | Prompt templates                     |
| 8. Testing          | 2-3 days | Phase 7      | Comprehensive test suite             |
| 9. Documentation    | 1-2 days | Phase 8      | Updated documentation                |
| 10. Deployment      | 1-2 days | Phase 9      | Production deployment                |

**Total Estimated Duration: 15-25 days**

---

## Next Steps

1. **Immediate Actions**:

   - Install FastMCP library: `pip install fastmcp`
   - Review FastMCP documentation thoroughly
   - Set up development branch for migration

2. **Phase 1 Execution**:

   - Complete current state assessment
   - Create new project structure
   - Begin configuration migration

3. **Stakeholder Communication**:
   - Notify users of upcoming changes
   - Provide migration timeline
   - Offer support during transition

This implementation plan provides a comprehensive roadmap for migrating the Agriculture MCP project from FastAPI to the FastMCP Python library, ensuring all functionality is preserved while gaining the benefits of proper MCP protocol implementation.
