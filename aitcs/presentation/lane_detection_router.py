"""HTTP adapter for the integrated AITCS perception path."""

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/v1/perception",
    tags=["Autonomous Lane Detection & Perception"],
)


class LaneTelemetryPayload(BaseModel):
    """Lane-departure and obstacle data from the AITCS perception subsystem."""

    intersection_id: str
    lane_departure_detected: bool
    curvature: float
    obstacle_risk_level: str


@router.post("/lane-telemetry")
async def ingest_lane_telemetry(payload: LaneTelemetryPayload):
    """Return the validated payload; no detection or persistence occurs here."""
    return {
        "status": "success",
        "processed_perception": payload.model_dump(),
    }
