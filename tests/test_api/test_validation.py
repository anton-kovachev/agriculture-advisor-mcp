import pytest
from datetime import datetime, timedelta
from app.core.schemas.advanced_validation import (
    CropManagementQuery,
    SoilAnalysisQuery,
    PestControlQuery,
    IrrigationScheduleQuery,
    HarvestTimingQuery,
    SoilType,
    ClimateZone,
    IrrigationMethod
)


def test_crop_management_validation():
    # Test valid wheat crop management
    valid_wheat = {
        "crop_type": "wheat",
        "planting_date": datetime.now() + timedelta(days=30),
        "field_size": 10.5,
        "soil_type": SoilType.LOAM,
        "climate_zone": ClimateZone.CONTINENTAL,
        "expected_rainfall": 300
    }
    CropManagementQuery(**valid_wheat)

    # Test invalid soil type for wheat
    invalid_wheat = valid_wheat.copy()
    invalid_wheat["soil_type"] = SoilType.SANDY
    with pytest.raises(ValueError, match="Wheat prefers loamy"):
        CropManagementQuery(**invalid_wheat)

    # Test valid corn crop management
    valid_corn = {
        "crop_type": "corn",
        "planting_date": datetime.now() + timedelta(days=30),
        "field_size": 20.0,
        "soil_type": SoilType.CLAY_LOAM,
        "climate_zone": ClimateZone.HUMID_SUBTROPICAL,
        "irrigation_method": IrrigationMethod.DRIP,
        "expected_rainfall": 200
    }
    CropManagementQuery(**valid_corn)

    # Test invalid climate for corn
    invalid_corn = valid_corn.copy()
    invalid_corn["climate_zone"] = ClimateZone.SUBARCTIC
    with pytest.raises(ValueError, match="Corn requires longer growing seasons"):
        CropManagementQuery(**invalid_corn)


def test_soil_analysis_validation():
    # Test valid soil analysis
    valid_soil = {
        "ph_level": 6.5,
        "organic_matter": 3.5,
        "nitrogen": 150,
        "phosphorus": 45,
        "potassium": 200,
        "soil_moisture": 60
    }
    SoilAnalysisQuery(**valid_soil)

    # Test invalid NPK levels
    invalid_soil = valid_soil.copy()
    invalid_soil["nitrogen"] = 600
    with pytest.raises(ValueError, match="Nitrogen level seems unreasonably high"):
        SoilAnalysisQuery(**invalid_soil)


def test_pest_control_validation():
    # Test valid pest control query
    valid_pest = {
        "pest_type": "aphids",
        "infestation_level": 3,
        "crop_stage": "flowering",
        "temperature": 25.5,
        "humidity": 65,
        "previous_treatments": ["neem_oil"]
    }
    result = PestControlQuery(**valid_pest)
    assert result.infestation_level["level"] == 3
    assert "Treatment recommended" in result.infestation_level["description"]


def test_irrigation_schedule_validation():
    # Test high urgency scenario
    high_urgency = {
        "crop_type": "corn",
        "growth_stage": "vegetative",
        "soil_moisture": 25,
        "expected_rainfall": 5,
        "temperature": 32,
        "humidity": 45,
        "wind_speed": 10
    }
    result = IrrigationScheduleQuery(**high_urgency)
    assert "High" in result.urgency


def test_harvest_timing_validation():
    # Test valid wheat harvest
    valid_harvest = {
        "crop_type": "wheat",
        "planting_date": datetime.now() - timedelta(days=120),
        "growing_degree_days": 2000,
        "grain_moisture": 15,
        "rainfall_forecast": 0
    }
    HarvestTimingQuery(**valid_harvest)

    # Test invalid moisture content
    invalid_harvest = valid_harvest.copy()
    invalid_harvest["grain_moisture"] = 20
    with pytest.raises(ValueError, match="Grain moisture too high"):
        HarvestTimingQuery(**invalid_harvest)
