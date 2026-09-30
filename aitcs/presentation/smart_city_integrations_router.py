"""HTTP adapters for simulated utility readings and citizen reports."""

from fastapi import APIRouter
from pydantic import BaseModel
from aitcs.application.smart_city_integrations_engine import SmartCityIntegrationsEngine

router = APIRouter(prefix="/api/v1/municipal-integrations", tags=["Smart City Municipal Integrations"])
engine = SmartCityIntegrationsEngine()

class CitizenReportPayload(BaseModel):
    """Category, description and coordinates submitted by a citizen."""

    category: str
    description: str
    latitude: float
    longitude: float

@router.get("/utilities/{station_id}")
async def get_utility_status(station_id: str):
    """Return fixed demonstration readings labelled with the requested station."""
    record = engine.monitor_utility_grid(station_id)
    return {"status": "success", "utility_record": record}

@router.post("/citizen-reports")
async def create_citizen_report(payload: CitizenReportPayload):
    """Store a report in process memory and return the created record."""
    report = engine.submit_citizen_report(
        payload.category,
        payload.description,
        payload.latitude,
        payload.longitude
    )
    return {"status": "success", "citizen_report": report}
