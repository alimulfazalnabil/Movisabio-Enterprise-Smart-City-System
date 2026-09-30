from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import get_db_session

app = FastAPI(
    title="MoviSabio Enterprise API",
    version="4.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
async def health_check(db: AsyncSession = Depends(get_db_session)):
    """Healthcheck endpoint."""
    # Check DB connectivity
    try:
        from sqlalchemy import text
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = "error"
    return {
        "status": "healthy",
        "database": db_status
    }

from apps.api.routers import perception
app.include_router(perception.router)
