"""HTTP adapter for V2X buffering and the local step simulator."""

from fastapi import APIRouter
from pydantic import BaseModel
from aitcs.application.digital_twin_v2x_engine import DigitalTwinV2XEngine, V2XBasicSafetyMessage

router = APIRouter(prefix="/api/v1/digital-twin", tags=["Digital Twin Simulation & V2X Gateway"])

twin_engine = DigitalTwinV2XEngine()

class BSMPayload(BaseModel):
    """Validated vehicle motion data for one basic safety message."""

    vehicle_id: str
    latitude: float
    longitude: float
    speed_ms: float
    heading_degrees: float
    acceleration_mps2: float
    intersection_id: str

@router.post("/v2x/bsm")
async def ingest_v2x_message(payload: BSMPayload):
    """Append a message to the process-local V2X buffer."""
    bsm = V2XBasicSafetyMessage(**payload.model_dump())
    twin_engine.ingest_v2x_bsm(bsm)
    return {"status": "success", "message": "V2X BSM ingested and queued for cooperative control."}

@router.get("/simulate/step")
async def trigger_simulation_step(engine_type: str = "SUMO"):
    """Advance simulated counters without contacting SUMO or CARLA."""
    state = twin_engine.sync_simulation_step(engine_type)
    return {"status": "success", "simulation_state": state}
