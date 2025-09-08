from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import weather_router, validation_router
from app.api.routes.agent import router as agent_router
from app.config import get_settings

app = FastAPI(
    title="Agriculture MCP",
    description="Model Context Protocol for Agriculture and Cereal Crop Farming",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Agriculture MCP API",
        "documentation": "/docs",
        "alternate_docs": "/redoc"
    }

# Include routers
app.include_router(weather_router, prefix="/api")
app.include_router(validation_router, prefix="/api")
app.include_router(agent_router, prefix="/api")


# Settings are now imported from app.config


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
