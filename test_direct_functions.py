#!/usr/bin/env python3
"""
Simple HTTP test client for Agriculture MCP Server
Tests server functionality via HTTP requests
"""
import asyncio
import httpx
import json
from typing import Dict, Any


class MCPHTTPTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def test_server_health(self):
        """Test if server is responding"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False

    async def list_tools(self):
        """List available MCP tools"""
        response = await self.client.post(
            f"{self.base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
        )
        return response.json()

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """Call an MCP tool"""
        response = await self.client.post(
            f"{self.base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
        )
        return response.json()

    async def list_resources(self):
        """List available MCP resources"""
        response = await self.client.post(
            f"{self.base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "resources/list",
                "params": {}
            }
        )
        return response.json()

    async def read_resource(self, uri: str):
        """Read an MCP resource"""
        response = await self.client.post(
            f"{self.base_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 4,
                "method": "resources/read",
                "params": {
                    "uri": uri
                }
            }
        )
        return response.json()


async def run_tests():
    """Run comprehensive tests of the Agriculture MCP server"""

    print("🧪 Testing Agriculture MCP Server (HTTP)")
    print("=" * 50)

    # Test with direct Python import instead
    print("📋 Testing server components directly...")

    # Import and test server components
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'src'))

        # Test imports
        from src.mcp_server import (
            get_crop_planting_advice,
            current_weather_resource,
            farming_advisor_prompt,
            test_connection,
            _check_soil_compatibility,
            _get_seasonal_notes
        )

        print("✅ Server modules imported successfully")

        # Test 1: Connection test
        print("\n🔌 Test 1: Connection Test")
        print("-" * 30)
        connection_result = await test_connection()
        print(f"Result: {connection_result}")

        # Test 2: Crop planting advice
        print("\n🌱 Test 2: Crop Planting Advice")
        print("-" * 30)

        test_args = {
            "crop_type": "corn",
            "soil_type": "loam",
            "latitude": 45.523064,
            "longitude": -122.676483,
            "planting_season": "spring"
        }

        advice_result = await get_crop_planting_advice(**test_args)

        print(f"Crop: {advice_result['crop_type'].title()}")
        print(
            f"Location: {advice_result['location']['latitude']}, {advice_result['location']['longitude']}")
        print(f"Soil Type: {advice_result['soil_type'].title()}")
        print(f"Season: {advice_result['season'].title()}")
        print("\nRecommendations:")
        for key, value in advice_result['recommendations'].items():
            print(f"  • {key.replace('_', ' ').title()}: {value}")
        print(f"\nNext Steps:")
        for i, step in enumerate(advice_result['next_steps'], 1):
            print(f"  {i}. {step}")

        # Test 3: Weather resource
        print("\n🌤️ Test 3: Weather Resource")
        print("-" * 30)

        weather_result = await current_weather_resource(45.523064, -122.676483)
        print("Weather data for Portland, OR:")
        print(weather_result)

        # Test 4: Farming advisor prompt
        print("\n👨‍🌾 Test 4: Farming Advisor Prompt")
        print("-" * 30)

        prompt_result = await farming_advisor_prompt("wheat", "Portland, Oregon", "planning")
        print("Farming advisor prompt template:")
        print(prompt_result[:300] + "...")

        # Test 5: Different combinations
        print("\n🔄 Test 5: Multiple Crop/Soil Combinations")
        print("-" * 30)

        test_combinations = [
            ("wheat", "clay", "fall"),
            ("sunflower", "sandy", "spring"),
            ("corn", "silt", "summer")
        ]

        for crop, soil, season in test_combinations:
            test_args = {
                "crop_type": crop,
                "soil_type": soil,
                "latitude": 40.7128,  # New York City
                "longitude": -74.0060,
                "planting_season": season
            }

            result = await get_crop_planting_advice(**test_args)
            compatibility = result['recommendations']['soil_compatibility']

            print(
                f"  • {crop.title()} + {soil.title()} soil ({season}): {compatibility}")

        # Test 6: Helper functions
        print("\n🔧 Test 6: Helper Functions")
        print("-" * 30)

        # Test soil compatibility function
        compatibility = _check_soil_compatibility("corn", "sandy")
        print(f"Corn + Sandy soil: {compatibility}")

        # Test seasonal notes function
        notes = _get_seasonal_notes("wheat", "fall")
        print(f"Wheat fall planting: {notes}")

        print("\n🎉 All direct tests completed successfully!")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error in direct testing: {e}")
        import traceback
        traceback.print_exc()


async def test_error_scenarios():
    """Test error handling scenarios"""
    print("\n🚨 Testing Error Handling")
    print("=" * 50)

    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'src'))

        from src.mcp_server import get_crop_planting_advice

        # Test 1: Invalid latitude (should be caught by Literal types)
        print("🔍 Testing boundary values...")

        # Test with extreme but valid coordinates
        extreme_args = {
            "crop_type": "corn",
            "soil_type": "loam",
            "latitude": 89.9,  # Near North Pole
            "longitude": 179.9,  # Near International Date Line
            "planting_season": "spring"
        }

        result = await get_crop_planting_advice(**extreme_args)
        print(f"✅ Extreme coordinates handled: {result['location']}")

        # Test 2: All crop/soil combinations
        print("\n🧪 Testing all crop/soil combinations...")

        crops = ["corn", "wheat", "sunflower"]
        soils = ["clay", "loam", "sandy", "silt"]
        seasons = ["spring", "summer", "fall"]

        combinations_tested = 0
        for crop in crops:
            for soil in soils:
                for season in seasons:
                    try:
                        test_args = {
                            "crop_type": crop,
                            "soil_type": soil,
                            "latitude": 45.0,
                            "longitude": -120.0,
                            "planting_season": season
                        }
                        result = await get_crop_planting_advice(**test_args)
                        combinations_tested += 1
                    except Exception as e:
                        print(
                            f"❌ Failed combination {crop}/{soil}/{season}: {e}")

        print(
            f"✅ Tested {combinations_tested}/{len(crops) * len(soils) * len(seasons)} combinations successfully")

    except Exception as e:
        print(f"❌ Error in error testing: {e}")


async def main():
    """Run all tests"""
    await run_tests()
    await test_error_scenarios()


if __name__ == "__main__":
    asyncio.run(main())
