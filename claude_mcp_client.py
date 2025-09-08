"""
Claude MCP Client for Agriculture API
This script demonstrates how to interact with the Agriculture MCP through ngrok for Claude integration.
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional


class AgricultureMCPClient:
    """Client for interacting with the Agriculture MCP API."""

    def __init__(self, mcp_base_url: str):
        """
        Initialize the MCP client.

        Args:
            mcp_base_url: Base URL of the MCP server (ngrok URL)
        """
        self.base_url = mcp_base_url.rstrip('/')
        self.session = requests.Session()
        # Add headers for ngrok if needed
        self.session.headers.update({
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': 'true'  # Skip ngrok browser warning
        })

    def test_connection(self) -> Dict[str, Any]:
        """Test if the MCP server is accessible."""
        try:
            response = self.session.get(f"{self.base_url}/")
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def initialize_context(self, latitude: float, longitude: float, task: str = "crop_planning") -> Dict[str, Any]:
        """
        Initialize agent context for farming location.

        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            task: Current farming task
        """
        url = f"{self.base_url}/api/agent/initialize"
        data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "current_task": task,
            "confidence_threshold": 0.8
        }

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_crop_management_advice(
        self,
        crop_type: str,
        soil_type: str,
        climate_zone: str,
        season: str,
        latitude: float = 40.7128,
        longitude: float = -74.0060
    ) -> Dict[str, Any]:
        """Get crop management recommendations."""
        url = f"{self.base_url}/api/agent/crop-management"

        data = {
            "query": {
                "crop_type": crop_type,
                "soil_type": soil_type,
                "climate_zone": climate_zone,
                "planting_season": season,
                "field_history": []
            },
            "context": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "location": {"latitude": latitude, "longitude": longitude},
                "current_task": "crop_management"
            }
        }

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_soil_analysis(
        self,
        ph_level: float,
        organic_matter: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        latitude: float = 40.7128,
        longitude: float = -74.0060
    ) -> Dict[str, Any]:
        """Get soil analysis recommendations."""
        url = f"{self.base_url}/api/agent/soil-analysis"

        data = {
            "query": {
                "soil_parameters": {
                    "ph_level": ph_level,
                    "organic_matter": organic_matter,
                    "nutrient_levels": {
                        "nitrogen": nitrogen,
                        "phosphorus": phosphorus,
                        "potassium": potassium
                    }
                }
            },
            "context": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "location": {"latitude": latitude, "longitude": longitude},
                "current_task": "soil_analysis"
            }
        }

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_irrigation_schedule(
        self,
        crop_type: str,
        growth_stage: str,
        soil_moisture: float,
        irrigation_method: str = "drip",
        latitude: float = 40.7128,
        longitude: float = -74.0060
    ) -> Dict[str, Any]:
        """Get irrigation recommendations."""
        url = f"{self.base_url}/api/agent/irrigation-schedule"

        data = {
            "query": {
                "crop_type": crop_type,
                "growth_stage": growth_stage,
                "soil_moisture": soil_moisture,
                "irrigation_method": irrigation_method,
                "weather_forecast": "variable"
            },
            "context": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "location": {"latitude": latitude, "longitude": longitude},
                "current_task": "irrigation_planning"
            }
        }

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_pest_control_advice(
        self,
        crop_type: str,
        growth_stage: str,
        pest_type: str,
        infestation_level: str,
        latitude: float = 40.7128,
        longitude: float = -74.0060
    ) -> Dict[str, Any]:
        """Get pest control recommendations."""
        url = f"{self.base_url}/api/agent/pest-control"

        data = {
            "query": {
                "crop_type": crop_type,
                "growth_stage": growth_stage,
                "pest_type": pest_type,
                "infestation_level": infestation_level,
                "treatment_history": []
            },
            "context": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "location": {"latitude": latitude, "longitude": longitude},
                "current_task": "pest_control"
            }
        }

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


def demo_agriculture_mcp(ngrok_url: str):
    """
    Demonstrate the Agriculture MCP capabilities.

    Args:
        ngrok_url: Your ngrok tunnel URL (e.g., https://abc123.ngrok-free.app)
    """
    print("🌾 Agriculture MCP Demo for Claude Integration")
    print("=" * 50)

    client = AgricultureMCPClient(ngrok_url)

    # Test connection
    print("\n1. Testing connection...")
    connection_test = client.test_connection()
    if connection_test["success"]:
        print("✅ Connected successfully!")
        print(f"Response: {connection_test['data']}")
    else:
        print("❌ Connection failed!")
        print(f"Error: {connection_test['error']}")
        return

    # Initialize context for a farm in Iowa
    print("\n2. Initializing context for Iowa farm...")
    iowa_lat, iowa_lon = 41.8781, -93.0977
    context_result = client.initialize_context(
        iowa_lat, iowa_lon, "comprehensive_planning")
    print(json.dumps(context_result, indent=2))

    # Get corn management advice
    print("\n3. Getting corn management advice...")
    corn_advice = client.get_crop_management_advice(
        crop_type="corn",
        soil_type="loam",
        climate_zone="temperate",
        season="spring",
        latitude=iowa_lat,
        longitude=iowa_lon
    )
    print(json.dumps(corn_advice, indent=2))

    # Get soil analysis
    print("\n4. Getting soil analysis...")
    soil_analysis = client.get_soil_analysis(
        ph_level=6.2,
        organic_matter=3.5,
        nitrogen=45.0,
        phosphorus=25.0,
        potassium=180.0,
        latitude=iowa_lat,
        longitude=iowa_lon
    )
    print(json.dumps(soil_analysis, indent=2))

    # Get irrigation schedule
    print("\n5. Getting irrigation schedule...")
    irrigation_advice = client.get_irrigation_schedule(
        crop_type="corn",
        growth_stage="V8",
        soil_moisture=65.0,
        irrigation_method="center_pivot",
        latitude=iowa_lat,
        longitude=iowa_lon
    )
    print(json.dumps(irrigation_advice, indent=2))

    # Get pest control advice
    print("\n6. Getting pest control advice...")
    pest_advice = client.get_pest_control_advice(
        crop_type="corn",
        growth_stage="V6",
        pest_type="corn_borer",
        infestation_level="low",
        latitude=iowa_lat,
        longitude=iowa_lon
    )
    print(json.dumps(pest_advice, indent=2))

    print("\n🎉 Demo completed! Your MCP is ready for Claude integration.")
    print("\nTo use with Claude, share your ngrok URL and ask Claude to help with farming decisions!")


if __name__ == "__main__":
    # Replace this with your actual ngrok URL
    NGROK_URL = "https://your-ngrok-url.ngrok-free.app"

    print("Please update the NGROK_URL variable with your actual ngrok tunnel URL")
    print("Example: https://abc123def456.ngrok-free.app")
    print("\nTo get your ngrok URL:")
    print("1. Start your MCP server: python -m uvicorn app.main:app --host 0.0.0.0 --port 5000")
    print("2. In another terminal: ngrok http 5000")
    print("3. Copy the https URL from ngrok output")

    # Uncomment the line below and add your ngrok URL to run the demo
    # demo_agriculture_mcp(NGROK_URL)
