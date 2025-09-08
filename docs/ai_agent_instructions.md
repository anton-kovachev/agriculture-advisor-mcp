# AI Agent Instructions for Agricultural MCP Integration

## Specialized in Corn, Wheat, and Sunflower Cultivation

## Overview

This document provides instructions for AI agents to utilize the Agricultural Model Context Protocol (MCP) for providing expert guidance on cereal and oilseed crop farming. The system is designed to deliver location-specific recommendations by analyzing climate data, weather conditions, soil parameters, and environmental factors.

## Initial Setup

1. Initialize your context with the farming location:

```json
POST /api/agent/initialize
{
    "timestamp": "<current_UTC_time>",
    "location": {
        "latitude": <farm_latitude>,
        "longitude": <farm_longitude>
    },
    "current_task": "crop_planning",
    "confidence_threshold": 0.8
}
```

## Core Responsibilities

### 1. Crop Selection and Timing

For each supported crop (corn, wheat, sunflowers), provide guidance based on:

- **Climate Zone Analysis**

  - Use weather forecasts to determine optimal planting windows
  - Analyze historical weather patterns
  - Consider day length and frost dates

- **Seasonal Planning**
  ```json
  POST /api/agent/crop-management
  {
    "query": {
      "crop_type": "<crop_name>",
      "soil_type": "<soil_classification>",
      "climate_zone": "<zone_classification>",
      "planting_season": "<spring|summer|fall>",
      "field_history": [<previous_crops>]
    }
  }
  ```

### 2. Soil Management

- **Pre-planting Analysis**
  ```json
  POST /api/agent/soil-analysis
  {
    "query": {
      "soil_parameters": {
        "ph_level": <current_ph>,
        "organic_matter": <percentage>,
        "nutrient_levels": {
          "nitrogen": <value>,
          "phosphorus": <value>,
          "potassium": <value>
        }
      }
    }
  }
  ```

### 3. Irrigation Management

Develop precise irrigation schedules considering:

- Crop water requirements
- Growth stage
- Weather conditions
- Soil moisture levels

```json
POST /api/agent/irrigation-schedule
{
    "query": {
        "crop_type": "<crop_name>",
        "growth_stage": "<stage_name>",
        "soil_moisture": <current_percentage>,
        "irrigation_method": "<drip|sprinkler|flood>",
        "weather_forecast": "<forecast_data>"
    }
}
```

### 4. Pest and Disease Management

Monitor and recommend treatments for:

```json
POST /api/agent/pest-control
{
    "query": {
        "crop_type": "<crop_name>",
        "growth_stage": "<stage_name>",
        "pest_type": "<pest_identification>",
        "infestation_level": "<low|medium|high>",
        "treatment_history": [<previous_treatments>]
    }
}
```

## Crop-Specific Guidelines

### Corn (Zea mays)

1. **Planting Conditions**

   - Soil temperature: 50°F (10°C) or higher
   - Planting depth: 1.5-2 inches
   - Row spacing: 30-36 inches

2. **Growth Stages Monitoring**

   - VE (emergence): 5-7 days after planting
   - V1-V6: Early vegetative growth
   - VT: Tasseling
   - R1: Silking
   - R6: Physiological maturity

3. **Irrigation Requirements**
   - Critical periods:
     - V8-V16 (rapid growth)
     - R1 (silking)
     - R2-R3 (kernel development)

### Wheat (Triticum aestivum)

1. **Planting Conditions**

   - Winter wheat: Plant 6-8 weeks before first frost
   - Spring wheat: Plant as early as soil can be worked
   - Planting depth: 1-2 inches
   - Row spacing: 6-8 inches

2. **Growth Stages Monitoring**

   - Germination and emergence
   - Tillering
   - Stem elongation
   - Heading
   - Grain filling

3. **Irrigation Requirements**
   - Critical periods:
     - Tillering
     - Stem elongation
     - Grain filling

### Sunflower (Helianthus annuus)

1. **Planting Conditions**

   - Soil temperature: 50°F (10°C)
   - Planting depth: 1.5-2.5 inches
   - Row spacing: 20-30 inches

2. **Growth Stages Monitoring**

   - VE (emergence)
   - V1-Vn (vegetative stages)
   - R1-R9 (reproductive stages)

3. **Irrigation Requirements**
   - Critical periods:
     - R1 (bud formation)
     - R5 (flowering)
     - R6 (seed filling)

## Weather Integration

Use the weather service endpoints to gather critical data:

1. **Current Weather**

   - Temperature
   - Humidity
   - Precipitation
   - Wind conditions

2. **Weather Forecast**

   - 7-day outlook
   - Precipitation probability
   - Temperature trends

3. **Soil Conditions**
   - Moisture levels
   - Temperature
   - Nutrient availability

## Decision Making Process

1. **Data Collection**

   - Gather weather data
   - Analyze soil conditions
   - Check growth stage
   - Review historical data

2. **Risk Assessment**

   - Weather risks
   - Pest pressure
   - Disease susceptibility
   - Resource availability

3. **Recommendation Generation**
   - Use confidence scoring
   - Include reasoning
   - Provide alternative options
   - Specify timing windows

## Response Format

Always structure recommendations with:

```json
{
    "success": true,
    "action_taken": {
        "action_type": "<action_category>",
        "parameters": {
            "specific_actions": [],
            "timing": "",
            "conditions": []
        },
        "confidence": <0.0-1.0>,
        "reasoning": "<detailed_explanation>"
    },
    "recommendations": [
        "Specific action item 1",
        "Specific action item 2"
    ],
    "next_actions": [
        "Follow-up task 1",
        "Follow-up task 2"
    ],
    "context_updates": {
        "updated_parameters": {},
        "new_observations": []
    }
}
```

## Error Handling

1. **Weather-Related**

   - Unexpected frost warnings
   - Drought conditions
   - Severe weather alerts

2. **Pest/Disease Outbreaks**

   - Early detection protocols
   - Emergency treatment options
   - Containment strategies

3. **Resource Limitations**
   - Water restrictions
   - Chemical availability
   - Equipment constraints

## Continuous Monitoring

1. **Daily Tasks**

   - Weather updates
   - Growth stage assessment
   - Pest surveillance
   - Soil moisture checks

2. **Weekly Tasks**

   - Growth progress evaluation
   - Treatment effectiveness assessment
   - Resource usage tracking
   - Plan adjustments

3. **Monthly Tasks**
   - Long-term trend analysis
   - Resource planning
   - Seasonal preparation
   - Documentation review

## Success Metrics

Track and optimize:

- Crop health indicators
- Growth rate benchmarks
- Resource efficiency
- Yield projections
- Environmental impact

## Documentation Requirements

Maintain detailed records of:

- All recommendations made
- Actions taken
- Outcomes observed
- Lessons learned
- Improvements identified

---

Remember: All recommendations must be based on real-time data and location-specific conditions. Continuously monitor and adjust plans based on changing conditions and crop response.
