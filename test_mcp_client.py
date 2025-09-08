import asyncio
from fastmcp import Client


async def test_agriculture_mcp():
    """Test the Agriculture MCP server with a simple client"""
    # Connect to HTTP server - note the /mcp endpoint
    client = Client("http://127.0.0.1:8000/mcp")

    async with client:
        print("=== Testing Agriculture MCP Server ===\n")

        # Test connection
        print("1. Testing connection...")
        result = await client.call_tool("test_connection", {})
        print(f"   Result: {result}\n")

        # Test crop planting advice tool
        print("2. Testing crop planting advice...")
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

        # Print the raw result for now
        print(f"   Tool Result: {result}")

        print("\n3. Testing weather resource...")
        # Test weather resource (this will be a basic test)
        try:
            print("   Weather resource will be tested once fully implemented")
        except Exception as e:
            print(f"   Note: {e}")

        print("\n=== All tests completed ===")

if __name__ == "__main__":
    asyncio.run(test_agriculture_mcp())
