# Connecting Agriculture MCP to Claude using Ngrok

This guide explains how to expose your local Agriculture MCP server to the internet using ngrok and connect it to Claude for AI-powered agricultural advice.

## Prerequisites

1. **Ngrok Account**: Sign up at [ngrok.com](https://ngrok.com)
2. **Ngrok CLI**: Download and install ngrok
3. **Running MCP Server**: Your Agriculture MCP should be running locally

## Step 1: Install and Setup Ngrok

### Install Ngrok

```powershell
# Option 1: Download from ngrok.com and extract to a folder in your PATH
# Option 2: Using Chocolatey
choco install ngrok

# Option 3: Using Scoop
scoop install ngrok
```

### Authenticate Ngrok

```powershell
# Get your auth token from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

## Step 2: Start Your MCP Server

```powershell
# Navigate to your project directory
cd C:\Users\user\Projects\agriculture-mcp

# Activate virtual environment and start server
.\.venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 5000
```

## Step 3: Expose Server with Ngrok

Open a new terminal window and run:

```powershell
# Expose your local server to the internet
ngrok http 5000
```

You'll see output like:

```
ngrok

Account:                       Your Name (Plan: Free)
Version:                       3.x.x
Region:                        United States (us)
Latency:                       -
Web Interface:                 http://127.0.0.1:4040
Forwarding:                    https://abc123def456.ngrok-free.app -> http://localhost:5000

Connections                    ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Important**: Copy the `https://abc123def456.ngrok-free.app` URL - this is your public endpoint.

## Step 4: Test Your Public API

Test that your API is accessible:

```powershell
# Test the root endpoint
curl https://abc123def456.ngrok-free.app/

# Test the API documentation
# Open in browser: https://abc123def456.ngrok-free.app/docs
```

## Step 5: Create Claude Integration Script

Create a Python script to demonstrate Claude integration:

```python
# claude_mcp_client.py
import requests
import json
from datetime import datetime

class AgricultureMCPClient:
    def __init__(self, mcp_base_url):
        self.base_url = mcp_base_url.rstrip('/')
        self.session = requests.Session()

    def initialize_context(self, latitude, longitude, task="crop_planning"):
        """Initialize agent context for farming location"""
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

        response = self.session.post(url, json=data)
        return response.json()

    def get_crop_management_advice(self, crop_type, soil_type, climate_zone, season):
        """Get crop management recommendations"""
        url = f"{self.base_url}/api/agent/crop-management"

        query_data = {
            "crop_type": crop_type,
            "soil_type": soil_type,
            "climate_zone": climate_zone,
            "planting_season": season,
            "field_history": []
        }

        context_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
            "current_task": "crop_management"
        }

        data = {
            "query": query_data,
            "context": context_data
        }

        response = self.session.post(url, json=data)
        return response.json()

    def get_irrigation_schedule(self, crop_type, growth_stage, soil_moisture):
        """Get irrigation recommendations"""
        url = f"{self.base_url}/api/agent/irrigation-schedule"

        query_data = {
            "crop_type": crop_type,
            "growth_stage": growth_stage,
            "soil_moisture": soil_moisture,
            "irrigation_method": "drip",
            "weather_forecast": "sunny"
        }

        context_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "location": {"latitude": 40.7128, "longitude": -74.0060},
            "current_task": "irrigation_planning"
        }

        data = {
            "query": query_data,
            "context": context_data
        }

        response = self.session.post(url, json=data)
        return response.json()

# Example usage
if __name__ == "__main__":
    # Replace with your ngrok URL
    MCP_URL = "https://abc123def456.ngrok-free.app"

    client = AgricultureMCPClient(MCP_URL)

    # Initialize context for a farm in Iowa
    print("Initializing context...")
    context_result = client.initialize_context(41.8781, -93.0977, "crop_planning")
    print(json.dumps(context_result, indent=2))

    # Get corn planting advice
    print("\nGetting corn management advice...")
    corn_advice = client.get_crop_management_advice(
        crop_type="corn",
        soil_type="loam",
        climate_zone="temperate",
        season="spring"
    )
    print(json.dumps(corn_advice, indent=2))

    # Get irrigation schedule
    print("\nGetting irrigation schedule...")
    irrigation_advice = client.get_irrigation_schedule(
        crop_type="corn",
        growth_stage="V8",
        soil_moisture=65.0
    )
    print(json.dumps(irrigation_advice, indent=2))
```

## Step 6: Claude Prompt Template

Use this prompt template when interacting with Claude:

```
I have an Agriculture MCP (Model Context Protocol) running at https://abc123def456.ngrok-free.app

This MCP provides expert agricultural advice for corn, wheat, and sunflower cultivation. It has the following endpoints:

1. POST /api/agent/initialize - Initialize farming context
2. POST /api/agent/crop-management - Get crop management advice
3. POST /api/agent/soil-analysis - Analyze soil conditions
4. POST /api/agent/pest-control - Get pest control recommendations
5. POST /api/agent/irrigation-schedule - Plan irrigation
6. POST /api/agent/harvest-timing - Determine harvest timing

Can you help me create a farming plan for [YOUR_SPECIFIC_REQUEST]? Please use the MCP endpoints to gather data and provide recommendations.

Location: [LATITUDE], [LONGITUDE]
Crop: [corn/wheat/sunflower]
Current conditions: [DESCRIBE YOUR SITUATION]
```

## Step 7: Example Claude Conversation

**You**: "I have an Agriculture MCP running at https://abc123def456.ngrok-free.app. I'm planning to plant corn in Iowa (41.8781, -93.0977) this spring. Can you help me create a comprehensive farming plan using the MCP?"

**Claude would then**:

1. Initialize context using the MCP
2. Get crop management advice for corn
3. Provide soil analysis recommendations
4. Create irrigation schedules
5. Suggest pest control measures
6. Plan harvest timing

## Step 8: Security Considerations

### For Production Use:

1. **Authentication**: Add API key authentication to your MCP
2. **Rate Limiting**: Implement rate limiting
3. **HTTPS**: Ensure all communications use HTTPS
4. **Monitoring**: Monitor API usage and performance

### Ngrok Security:

```powershell
# Use password protection
ngrok http 5000 --basic-auth="username:password"

# Use custom domain (paid plan)
ngrok http 5000 --domain=yourdomain.ngrok.io
```

## Step 9: Monitoring and Debugging

### View Ngrok Traffic:

- Open http://127.0.0.1:4040 in your browser
- Monitor all HTTP requests and responses
- Debug API calls in real-time

### Server Logs:

Monitor your FastAPI server logs for:

- Request details
- Response times
- Error messages
- Usage patterns

## Troubleshooting

### Common Issues:

1. **Connection Refused**

   - Ensure your MCP server is running on port 5000
   - Check firewall settings

2. **Ngrok Tunnel Closed**

   - Restart ngrok tunnel
   - Check ngrok authentication

3. **API Errors**
   - Verify JSON payload format
   - Check API documentation at `/docs`
   - Review server logs

### Testing Commands:

```powershell
# Test server locally
curl http://localhost:5000/

# Test through ngrok
curl https://your-ngrok-url.ngrok-free.app/

# Test specific endpoints
curl -X POST https://your-ngrok-url.ngrok-free.app/api/agent/initialize \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2025-09-08T10:00:00Z","location":{"latitude":41.8781,"longitude":-93.0977},"current_task":"crop_planning"}'
```

## Next Steps

1. **Enhance Security**: Add authentication and rate limiting
2. **Custom Domain**: Consider ngrok paid plans for custom domains
3. **Production Deployment**: Deploy to cloud services for permanent availability
4. **Integration**: Build web interfaces or mobile apps using the API
5. **Monitoring**: Implement comprehensive logging and monitoring

Remember to keep your ngrok URL private and consider the security implications of exposing your local server to the internet.
