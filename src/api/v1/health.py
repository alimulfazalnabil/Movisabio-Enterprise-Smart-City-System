from fastapi import APIRouter, Depends, HTTPException
from src.auth.dependencies import require_permission
from typing import Dict

router = APIRouter(prefix="/health", tags=["observability"])

# 1. Liveness Probe (Kubernetes/Docker health check)
# Answers: Is the process alive?
@router.get("/live")
async def health_live():
    return {"status": "alive"}

# 2. Readiness Probe
# Answers: Can this instance serve traffic?
@router.get("/ready")
async def health_ready():
    # In a full implementation, check if critical threadpools or internal states are fully loaded
    return {"status": "ready"}

# 3. Startup Probe
# Answers: Has initialization completed?
@router.get("/startup")
async def health_startup():
    return {"status": "initialized"}

# 4. Dependency Health (Protected, internal SRE endpoint)
@router.get("/dependencies", dependencies=[Depends(require_permission("audit.admin"))])
async def check_dependencies() -> Dict[str, str]:
    """
    Deep diagnostic health check. Verifies external connections.
    """
    dependencies = {
        "postgresql": "healthy", # Mocked
        "redis": "healthy", # Mocked
        "message_bus": "unknown",
        "object_storage": "unknown"
    }
    
    # In reality, this would execute `db.execute('SELECT 1')` or `redis.ping()`
    
    if "degraded" in dependencies.values() or "down" in dependencies.values():
        raise HTTPException(status_code=503, detail={"status": "degraded", "dependencies": dependencies})
        
    return {"status": "ok", "dependencies": dependencies}
