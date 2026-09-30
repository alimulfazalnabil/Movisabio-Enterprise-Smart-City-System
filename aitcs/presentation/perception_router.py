"""AITCS endpoints for perception-frame ingestion and recent history."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from aitcs.application.perception_bridge_engine import PerceptionBridgeEngine


router = APIRouter(
    prefix="/api/v1/perception",
    tags=["Autonomous Lane Detection & Perception Bridge"],
)
engine = PerceptionBridgeEngine()


class PerceptionPayload(BaseModel):
    """Validated sensor-fusion values for one vehicle frame."""

    intersection_id: str
    vehicle_id: str
    lane_departure_detected: bool
    curvature_radius: float
    collision_risk_score: float = Field(ge=0.0, le=1.0)
    fused_objects_count: int = Field(ge=0)


@router.post("/telemetry/ingest")
async def ingest_perception_telemetry(payload: PerceptionPayload):
    """Store one frame in process memory and return its safety classification."""
    record = engine.process_perception_frame(
        intersection_id=payload.intersection_id,
        vehicle_id=payload.vehicle_id,
        lane_departure=payload.lane_departure_detected,
        curvature=payload.curvature_radius,
        risk_score=payload.collision_risk_score,
        objects_count=payload.fused_objects_count,
    )
    safety_evaluation = engine.evaluate_safety_threshold(record)

    return {
        "status": "success",
        "perception_record": record,
        "safety_evaluation": safety_evaluation,
    }


@router.get("/history/{intersection_id}")
async def get_intersection_perception_history(intersection_id: str):
    """Return at most 50 recent in-process records for an intersection."""
    filtered_records = [
        record
        for record in engine.telemetry_history
        if record.intersection_id == intersection_id
    ]
    return {
        "status": "success",
        "intersection_id": intersection_id,
        "total_records": len(filtered_records),
        "records": filtered_records[-50:],
    }
