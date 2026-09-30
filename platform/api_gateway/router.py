from fastapi import APIRouter
from platform.identity import auth
from platform.database import session
from platform.config import settings

# This defines the standard entry point for all platform modules
api_router = APIRouter()

@api_router.get("/health")
def health_check():
    return {"status": "ONLINE", "service": "MoviSabio Control Plane"}
