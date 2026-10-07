from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.app.config import settings

from contextlib import asynccontextmanager
from backend.app.database.session import engine
from backend.app.models.traffic import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MoviSabio Enterprise Traffic Intelligence Platform",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}

@app.get("/health/live")
async def liveness_check():
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness_check():
    # In future, check DB and Redis connectivity here
    return {"status": "ready"}

from backend.app.api.v1 import cameras, traffic
from backend.app.api.v1.endpoints import mobility, environment, infrastructure, resilience, civic, economy, spatial, resources, circular, agriculture, health, human_capital

app.include_router(cameras.router, prefix="/api/v1/cameras", tags=["cameras"])
app.include_router(traffic.router, prefix="/api/v1", tags=["traffic"])
app.include_router(mobility.router, prefix="/api/v1/mobility", tags=["mobility"])
app.include_router(environment.router, prefix="/api/v1/environment", tags=["environment"])
app.include_router(infrastructure.router, prefix="/api/v1/infrastructure", tags=["infrastructure"])
app.include_router(resilience.router, prefix="/api/v1/resilience", tags=["resilience"])
app.include_router(civic.router, prefix="/api/v1/civic", tags=["civic"])
app.include_router(economy.router, prefix="/api/v1/economy", tags=["economy"])
app.include_router(spatial.router, prefix="/api/v1/spatial", tags=["spatial"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["resources"])
app.include_router(circular.router, prefix="/api/v1/circular", tags=["circular"])
app.include_router(agriculture.router, prefix="/api/v1/agriculture", tags=["agriculture"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(human_capital.router, prefix="/api/v1/human-capital", tags=["human-capital"])
