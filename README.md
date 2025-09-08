_# agriculture-advisor-mcp
An MCP server that turns yor AI agent into a corn and wheat farming specialist.

To set it up and running first in the main project directory add an .env file with the following keys

### API Keys
AGROMONITORING_API_KEY=your_agro_monitoring_api_key_here
WEATHER_COMPANY_API_KEY=your_weather_company_api_key_here

### API Base URLs
AGROMONITORING_BASE_URL=http://api.agromonitoring.com/agro/1.0
WEATHER_COMPANY_BASE_URL=https://api.weather.com/v2


### Run the MCP server
python.exe src/mcp_server.py --http --port=8000


### ngrok
Install ngrok and route it to port 8000 via http and obtain an ngrok url


### Install Claude Code

Install Claude Code AI agent and attach the MCP server to it with the following command 
claude mcp add --transport http agriculture-advisor {ngrok_url}

### Open Claude

Open Claude AI agent by just typing the claud command and receiver expert corn, wheat and sunflower farming advices from your agriculture specialist.





_
