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
from backend.app.api.v1.endpoints import mobility, environment, infrastructure, resilience, civic, economy, spatial, resources, circular, agriculture, health, human_capital, tourism, industry, buildings, digital_infrastructure, security, trust, finance, regulatory, justice, government, international, strategic, national_resilience, climate_futures, population, social, science_innovation, digital_economy, agents, marketplace, digital_twins, quantum, global_federation, enterprise, sre, governance, mlops, integration

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
app.include_router(tourism.router, prefix="/api/v1/tourism", tags=["tourism"])
app.include_router(industry.router, prefix="/api/v1/industry", tags=["industry"])
app.include_router(buildings.router, prefix="/api/v1/buildings", tags=["buildings"])
app.include_router(digital_infrastructure.router, prefix="/api/v1/digital-infrastructure", tags=["digital-infrastructure"])
app.include_router(security.router, prefix="/api/v1/security", tags=["security"])
app.include_router(trust.router, prefix="/api/v1/trust", tags=["trust"])
app.include_router(finance.router, prefix="/api/v1/finance", tags=["finance"])
app.include_router(regulatory.router, prefix="/api/v1/regulatory", tags=["regulatory"])
app.include_router(justice.router, prefix="/api/v1/justice", tags=["justice"])
app.include_router(government.router, prefix="/api/v1/government", tags=["government"])
app.include_router(international.router, prefix="/api/v1/international", tags=["international"])
app.include_router(strategic.router, prefix="/api/v1/strategic", tags=["strategic"])
app.include_router(national_resilience.router, prefix="/api/v1/national-resilience", tags=["national-resilience"])
app.include_router(climate_futures.router, prefix="/api/v1/climate", tags=["climate"])
app.include_router(population.router, prefix="/api/v1/population", tags=["population"])
app.include_router(social.router, prefix="/api/v1/social", tags=["social"])
app.include_router(science_innovation.router, prefix="/api/v1/science-innovation", tags=["science-innovation"])
app.include_router(digital_economy.router, prefix="/api/v1/digital-economy", tags=["digital-economy"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(marketplace.router, prefix="/api/v1/marketplace", tags=["marketplace"])
app.include_router(digital_twins.router, prefix="/api/v1/twins", tags=["digital-twins"])
app.include_router(quantum.router, prefix="/api/v1/quantum", tags=["quantum"])
app.include_router(global_federation.router, prefix="/api/v1/global", tags=["global-federation"])
app.include_router(enterprise.router, prefix="/api/v1/enterprise", tags=["enterprise"])
app.include_router(sre.router, prefix="/api/v1/sre", tags=["sre"])
app.include_router(governance.router, prefix="/api/v1/governance", tags=["governance"])
app.include_router(mlops.router, prefix="/api/v1/mlops", tags=["mlops"])
app.include_router(integration.router, prefix="/api/v1/integration", tags=["integration"])
