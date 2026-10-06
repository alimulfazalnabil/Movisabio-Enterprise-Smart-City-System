from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MoviSabio Enterprise Traffic Intelligence Platform"
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
