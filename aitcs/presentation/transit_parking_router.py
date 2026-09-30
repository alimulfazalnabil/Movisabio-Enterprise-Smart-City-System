"""HTTP adapters for transit priority and demonstration parking data."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from aitcs.application.public_transport_engine import TransitSignalPriorityEngine, TransitPriorityRequest
from aitcs.application.smart_parking_engine import SmartParkingEngine

router = APIRouter(prefix="/api/v1/transit-parking", tags=["Public Transport & Smart Parking"])

tsp_engine = TransitSignalPriorityEngine()
parking_engine = SmartParkingEngine()

class TSPPayload(BaseModel):
    """Transit arrival data used to evaluate signal priority."""

    vehicle_id: str
    transit_type: str
    intersection_id: str
    route_number: str
    estimated_arrival_seconds: int
    passenger_count: int

@router.post("/tsp/evaluate")
async def evaluate_transit_priority(payload: TSPPayload):
    """Return the rule-based priority decision for a transit arrival."""
    req = TransitPriorityRequest(**payload.model_dump())
    decision = tsp_engine.evaluate_transit_priority(req)
    return {"status": "success", "decision": decision}

@router.get("/parking/{zone_id}")
async def get_parking_status(zone_id: str):
    """Return built-in occupancy data or the engine's generic fallback."""
    status = parking_engine.get_zone_status(zone_id)
    return {"status": "success", "parking_zone": status}
