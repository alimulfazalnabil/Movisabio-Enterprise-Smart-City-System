"""Compose the FastAPI gateway that is served by the main container.

Only routers included in :func:`create_unified_enterprise_platform` are exposed
by this process. Standalone apps under ``backend.services`` run separately.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from aitcs.presentation.api_router import router as aitcs_router
from aitcs.presentation.lane_detection_router import router as lane_detection_router
from aitcs.presentation.perception_router import router as perception_router
from aitcs.config import settings

def create_unified_enterprise_platform() -> FastAPI:
    """Build the gateway application and register its public routers.

    Returns:
        A configured FastAPI application. No network or database connection is
        opened while the application is being assembled.
    """
    app = FastAPI(
        title="MoviSabio Enterprise Smart City & Autonomous Perception Platform",
        version="3.3.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount AITCS & Advanced Subsystem Router (Traffic, CV/ANPR, Environment, Incidents)
    app.include_router(aitcs_router)
    app.include_router(lane_detection_router)
    app.include_router(perception_router)

    @app.get("/api/v1/smart-city/status", tags=["Smart City Core"])
    async def smart_city_system_status():
        """Return a descriptive platform status; it does not probe dependencies."""
        return {
            "platform": "MoviSabio Enterprise Smart City with Autonomous Perception",
            "modules_active": [
                "Core Gateway & API Router",
                "AI Traffic Control System (AITCS)",
                "Computer Vision & ANPR Engine",
                "Environmental & Weather Intelligence",
                "Incident Detection & Emergency Routing",
                "Autonomous Lane Detection & Sensor Fusion Bridge",
                "PostGIS Spatial Repository"
            ],
            "environment": settings.environment,
            "status": "operational"
        }

    @app.get("/api/v1/observability/health", tags=["Observability"])
    async def global_health_check():
        """Return gateway process health without checking Redis or PostgreSQL."""
        return {
            "status": "healthy",
            "system": settings.app_name,
            "environment": settings.environment,
            "version": "3.3.0-production",
            "unified_runtime": "active"
        }

    return app

app = create_unified_enterprise_platform()
