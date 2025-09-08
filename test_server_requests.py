#!/usr/bin/env python3
"""
Test client for Agriculture MCP Server
Tests the current server functionality with sample requests
"""
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from typing import Any, Dict
import json
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


async def test_mcp_server():
    """Test the Agriculture MCP server with various requests"""

    print("🧪 Testing Agriculture MCP Server")
    print("=" * 50)

    # Server parameters - using the virtual environment Python
    server_params = StdioServerParameters(
        command="C:/Users/user/Projects/agriculture-mcp/.venv/Scripts/python.exe",
        args=["src/mcp_server.py"]
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:

                # Initialize the session
                await session.initialize()

                print("✅ Server connection established")
                print()

                # Test 1: List available tools
                print("📋 Test 1: List Available Tools")
                print("-" * 30)

                tools_result = await session.list_tools()
                print(f"Available tools ({len(tools_result.tools)}):")
                for tool in tools_result.tools:
                    print(f"  • {tool.name}: {tool.description}")
                print()

                # Test 2: List available resources
                print("📚 Test 2: List Available Resources")
                print("-" * 30)

                resources_result = await session.list_resources()
                print(
                    f"Available resources ({len(resources_result.resources)}):")
                for resource in resources_result.resources:
                    print(f"  • {resource.uri}: {resource.description}")
                print()

                # Test 3: List available prompts
                print("💬 Test 3: List Available Prompts")
                print("-" * 30)

                prompts_result = await session.list_prompts()
                print(f"Available prompts ({len(prompts_result.prompts)}):")
                for prompt in prompts_result.prompts:
                    print(f"  • {prompt.name}: {prompt.description}")
                print()

                # Test 4: Test connection tool
                print("🔌 Test 4: Test Connection Tool")
                print("-" * 30)

                connection_result = await session.call_tool("test_connection", {})
                print(
                    f"Connection test result: {connection_result.content[0].text}")
                print()

                # Test 5: Test crop planting advice tool
                print("🌱 Test 5: Crop Planting Advice Tool")
                print("-" * 30)

                planting_args = {
                    "crop_type": "corn",
                    "soil_type": "loam",
                    "latitude": 45.523064,
                    "longitude": -122.676483,
                    "planting_season": "spring"
                }

                planting_result = await session.call_tool("get_crop_planting_advice", planting_args)
                advice_data = json.loads(planting_result.content[0].text)

                print(f"Crop: {advice_data['crop_type'].title()}")
                print(
                    f"Location: {advice_data['location']['latitude']}, {advice_data['location']['longitude']}")
                print(f"Soil Type: {advice_data['soil_type'].title()}")
                print(f"Season: {advice_data['season'].title()}")
                print("\nRecommendations:")
                for key, value in advice_data['recommendations'].items():
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
                print(f"\nNext Steps:")
                for i, step in enumerate(advice_data['next_steps'], 1):
                    print(f"  {i}. {step}")
                print()

                # Test 6: Test weather resource
                print("🌤️ Test 6: Weather Resource")
                print("-" * 30)

                weather_uri = "weather://current/45.523064/-122.676483"
                weather_result = await session.read_resource(weather_uri)
                print(f"Weather data for Portland, OR:")
                print(weather_result.contents[0].text)

                # Test 7: Test farming advisor prompt
                print("👨‍🌾 Test 7: Farming Advisor Prompt")
                print("-" * 30)

                prompt_args = {
                    "crop_type": "wheat",
                    "location": "Portland, Oregon",
                    "growth_stage": "planning"
                }

                prompt_result = await session.get_prompt("farming-advisor", prompt_args)
                print("Farming advisor prompt template:")
                print(prompt_result.messages[0].content.text[:300] + "...")
                print()

                # Test 8: Test different crop types and soil combinations
                print("🔄 Test 8: Multiple Crop/Soil Combinations")
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

                    result = await session.call_tool("get_crop_planting_advice", test_args)
                    data = json.loads(result.content[0].text)
                    compatibility = data['recommendations']['soil_compatibility']

                    print(
                        f"  • {crop.title()} + {soil.title()} soil ({season}): {compatibility}")

                print()
                print("🎉 All tests completed successfully!")
                print("=" * 50)

    except Exception as e:
        print(f"❌ Error testing server: {e}")
        import traceback
        traceback.print_exc()


async def test_error_handling():
    """Test error handling with invalid inputs"""

    print("\n🚨 Testing Error Handling")
    print("=" * 50)

    server_params = StdioServerParameters(
        command="C:/Users/user/Projects/agriculture-mcp/.venv/Scripts/python.exe",
        args=["src/mcp_server.py"]
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Test invalid crop type
                print("🔍 Testing invalid crop type...")
                try:
                    invalid_args = {
                        "crop_type": "invalid_crop",
                        "soil_type": "loam",
                        "latitude": 45.0,
                        "longitude": -122.0,
                        "planting_season": "spring"
                    }
                    await session.call_tool("get_crop_planting_advice", invalid_args)
                    print("❌ Should have failed with invalid crop type")
                except Exception as e:
                    print(
                        f"✅ Correctly caught invalid crop type: {type(e).__name__}")

                # Test invalid coordinates
                print("🔍 Testing invalid coordinates...")
                try:
                    invalid_args = {
                        "crop_type": "corn",
                        "soil_type": "loam",
                        "latitude": 999.0,  # Invalid latitude
                        "longitude": -122.0,
                        "planting_season": "spring"
                    }
                    await session.call_tool("get_crop_planting_advice", invalid_args)
                    print("❌ Should have failed with invalid coordinates")
                except Exception as e:
                    print(
                        f"✅ Correctly caught invalid coordinates: {type(e).__name__}")

                # Test invalid resource URI
                print("🔍 Testing invalid resource URI...")
                try:
                    await session.read_resource("invalid://resource/uri")
                    print("❌ Should have failed with invalid resource")
                except Exception as e:
                    print(
                        f"✅ Correctly caught invalid resource: {type(e).__name__}")

                print("✅ Error handling tests completed")

    except Exception as e:
        print(f"❌ Error in error handling tests: {e}")


async def main():
    """Run all tests"""
    await test_mcp_server()
    await test_error_handling()


if __name__ == "__main__":
    asyncio.run(main())
