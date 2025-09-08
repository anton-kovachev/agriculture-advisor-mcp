# Advanced Validation API

This document describes the advanced validation endpoints available in the Agriculture MCP API.

## Endpoints

### 1. Crop Management Validation

`POST /validate/crop-management`

Validates crop management parameters including:

- Crop type compatibility with soil and climate
- Planting date validation
- Field size validation
- Previous crop consideration
- Irrigation requirements

### 2. Soil Analysis Validation

`POST /validate/soil-analysis`

Validates soil test results including:

- pH levels (0-14)
- Organic matter content (0-100%)
- NPK levels
- Soil moisture content

### 3. Pest Control Validation

`POST /validate/pest-control`

Validates pest control parameters including:

- Pest type identification
- Infestation level assessment (1-5)
- Environmental conditions
- Treatment history

### 4. Irrigation Schedule Validation

`POST /validate/irrigation-schedule`

Validates irrigation parameters including:

- Crop water requirements
- Soil moisture levels
- Weather conditions
- Irrigation timing

### 5. Harvest Timing Validation

`POST /validate/harvest-timing`

Validates harvest timing parameters including:

- Growing degree days
- Grain moisture content
- Weather conditions
- Crop maturity indicators

## Example Requests

### Crop Management

```json
{
  "crop_type": "wheat",
  "planting_date": "2025-10-01T00:00:00",
  "field_size": 10.5,
  "soil_type": "loam",
  "climate_zone": "continental",
  "expected_rainfall": 300
}
```

### Soil Analysis

```json
{
  "ph_level": 6.5,
  "organic_matter": 3.5,
  "nitrogen": 150,
  "phosphorus": 45,
  "potassium": 200,
  "soil_moisture": 60
}
```

### Pest Control

```json
{
  "pest_type": "aphids",
  "infestation_level": 3,
  "crop_stage": "flowering",
  "temperature": 25.5,
  "humidity": 65,
  "previous_treatments": ["neem_oil"]
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- 200: Successful validation
- 400: Invalid input parameters
- 404: Resource not found
- 500: Server error

Error responses include a detail message explaining the validation failure.
