"""HTTP adapter for combined vision, environment and incident analysis."""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from datetime import datetime
import asyncio
import json

from aitcs.application.cv_anpr_engine import ComputerVisionANPREngine
from aitcs.application.environmental_weather_engine import EnvironmentalWeatherEngine
from aitcs.application.incident_emergency_engine import IncidentEmergencyEngine

router = APIRouter(prefix="/api/v1/aitcs", tags=["AI Traffic Control System & Smart City Modules"])

cv_engine = ComputerVisionANPREngine()
env_engine = EnvironmentalWeatherEngine()
incident_engine = IncidentEmergencyEngine()

class TelemetryPayload(BaseModel):
    """Combined telemetry accepted by the AITCS analysis endpoint."""

    intersection_id: str
    vehicle_count: int
    pedestrian_count: int
    average_speed_kmh: float
    weather_condition: str = "CLEAR"
    plates: list = []
    wrong_way_detected: bool = False
    sudden_stoppage_count: int = 0

@router.post("/telemetry/analyze")
async def analyze_full_telemetry(payload: TelemetryPayload):
    """Run the three stateless analysis engines and return their typed results."""
    payload_data = payload.model_dump()
    cv_result = cv_engine.process_frame_telemetry(payload.intersection_id, payload_data)
    env_result = env_engine.compute_environmental_impact(payload.intersection_id, payload.vehicle_count, payload.average_speed_kmh, payload.weather_condition)
    incidents = incident_engine.detect_incidents(payload.intersection_id, payload_data)
    
    return {
        "status": "success",
        "computer_vision": cv_result,
        "environmental_impact": env_result,
        "detected_incidents": incidents,
        "timestamp": datetime.utcnow()
    }
