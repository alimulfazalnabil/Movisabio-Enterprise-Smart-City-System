"""Standalone FastAPI service for adaptive street-lighting commands."""

import os
import time
import logging
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MoviSabio.StreetlightingOptimization")

app = FastAPI(
    title="MoviSabio Smart Streetlighting & Adaptive Luminance Gateway",
    version="1.0.0",
    description="Ingests smart luminaire telemetry and computes dynamic adaptive dimming profiles to optimize energy usage."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class StreetlightTelemetryPayload(BaseModel):
    """Ambient, motion and electrical readings for one lighting zone."""

    node_id: str
    district_id: str
    ambient_lux: float
    pedestrian_motion_detected: bool
    vehicle_count_nearby: int
    current_power_draw_w: float
    led_temperature_c: float


class StreetlightOverrideRequest(BaseModel):
    """Manual brightness override requested for a lighting zone."""

    district_id: str
    target_dimming_percentage: float
    override_reason: str


class StreetlightingOptimizationEngine:
    """Evaluates ambient light and motion telemetry to calculate optimal LED luminaire dimming percentages."""
    def __init__(self, base_power_w: float = 150.0, minimum_dimming_pct: float = 30.0):
        self.base_power = base_power_w
        self.min_dimming = minimum_dimming_pct

    def compute_adaptive_luminance(self, payload: StreetlightTelemetryPayload) -> Dict[str, Any]:
        """Calculates dynamic dimming levels based on ambient daylight, pedestrian motion, and traffic density."""
        logger.info(f"Computing adaptive luminance for streetlight node {payload.node_id} in district {payload.district_id}...")

        # Daylight threshold check: if ambient light exceeds 50 lux, turn luminaires off (0% dimming)
        if payload.ambient_lux >= 50.0:
            target_dimming = 0.0
            operational_mode = "DAYLIGHT_OFF"
        elif payload.pedestrian_motion_detected or payload.vehicle_count_nearby > 0:
            # Full luminance when activity or traffic is detected
            target_dimming = 100.0
            operational_mode = "ACTIVE_TRAFFIC_LUMINANCE"
            logger.info(f"💡 Motion/Traffic detected near node {payload.node_id}. Ramping luminaire to 100%.")
        else:
            # Eco-dimming mode during late night hours with zero detected movement
            target_dimming = self.min_dimming
            operational_mode = "ECO_DIMMING_ACTIVE"

        # Calculate estimated power consumption under adaptive dimming
        estimated_power_draw = self.base_power * (target_dimming / 100.0)
        energy_savings_pct = max(0.0, 100.0 - target_dimming)

        report = {
            "node_id": payload.node_id,
            "district_id": payload.district_id,
            "ambient_lux": payload.ambient_lux,
            "operational_mode": operational_mode,
            "target_dimming_percentage": target_dimming,
            "estimated_power_draw_w": round(estimated_power_draw, 2),
            "energy_savings_percentage": energy_savings_pct,
            "led_temperature_c": payload.led_temperature_c,
            "timestamp": time.time()
        }
        return report

    def override_district_lighting(self, req: StreetlightOverrideRequest) -> Dict[str, Any]:
        """Manages municipal district-wide manual lighting override commands (e.g., public safety events or maintenance)."""
        logger.info(f"Executing district override for {req.district_id} (Target Dimming: {req.target_dimming_percentage}%, Reason: {req.override_reason})...")
        
        override_result = {
            "district_id": req.district_id,
            "target_dimming_percentage": req.target_dimming_percentage,
            "override_reason": req.override_reason,
            "status": "DISTRICT_LIGHTING_OVERRIDE_ACTIVE",
            "timestamp": time.time()
        }
        return override_result


lighting_engine = StreetlightingOptimizationEngine(base_power_w=150.0, minimum_dimming_pct=30.0)


@app.post("/api/v1/infrastructure/streetlighting/telemetry", status_code=status.HTTP_200_OK)
def api_process_lighting_telemetry(payload: StreetlightTelemetryPayload):
    """API endpoint for smart luminaire nodes to report live environmental metrics and receive dimming commands."""
    try:
        report = lighting_engine.compute_adaptive_luminance(payload)
        
        # Cache active node dimming state in Redis for fast edge controller synchronization
        cache_key = f"infrastructure:streetlight:node:{payload.node_id}"
        redis_client.hset(cache_key, mapping={
            "dimming_pct": report["target_dimming_percentage"],
            "mode": report["operational_mode"],
            "power_w": report["estimated_power_draw_w"],
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 600)  # Valid for 10 minutes

        return {
            "status": "success",
            "lighting_assessment_report": report
        }
    except Exception as e:
        logger.error(f"Streetlighting telemetry processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/infrastructure/streetlighting/override", status_code=status.HTTP_200_OK)
def api_override_district_lighting(req: StreetlightOverrideRequest):
    """API endpoint to execute emergency or maintenance lighting overrides across municipal districts."""
    try:
        result = lighting_engine.override_district_lighting(req)
        return {
            "status": "success",
            "district_override_result": result
        }
    except Exception as o_err:
        logger.error(f"District lighting override failed: {o_err}")
        raise HTTPException(status_code=500, detail=str(o_err))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("streetlighting_optimization:app", host="0.0.0.0", port=8027, reload=True)
