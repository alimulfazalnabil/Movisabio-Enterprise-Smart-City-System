"""HTTP adapter for the process-local demonstration drone fleet."""

from fastapi import APIRouter, HTTPException
from aitcs.application.drone_operations_engine import DroneOperationsEngine

drone_router = APIRouter(prefix="/api/v1/drones", tags=["Drone Operations & Aerial Intelligence"])
drone_engine = DroneOperationsEngine()

@drone_router.get("/fleet")
async def get_drone_fleet_status():
    """Return the current in-process fleet snapshot."""
    return {
        "status": "success",
        "fleet_size": len(drone_engine.fleet),
        "units": drone_engine.get_fleet_telemetry()
    }

@drone_router.post("/dispatch")
async def dispatch_drone(target_intersection_id: str, mission_type: str = "INCIDENT_RECONNAISSANCE"):
    """Create a simulated mission or return HTTP 503 when no drone is eligible."""
    mission = drone_engine.dispatch_reconnaissance_drone(target_intersection_id, mission_type)
    if not mission:
        raise HTTPException(status_code=503, detail="No available drone units in standby with sufficient battery.")
    return {
        "status": "success",
        "mission": mission
    }
