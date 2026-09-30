"""Standalone FastAPI service for municipal fleet telemetry."""

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
logger = logging.getLogger("MoviSabio.FleetTelematics")

app = FastAPI(
    title="MoviSabio Municipal Fleet GPS & Telematics Tracking Gateway",
    version="1.0.0",
    description="Ingests live municipal vehicle GPS coordinates, evaluates driver behavior, and tracks fleet telemetry."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class VehicleTelemetryPayload(BaseModel):
    """Position, fuel and diagnostics reported by a fleet vehicle."""

    vehicle_id: str
    fleet_type: str  # e.g., "SANITATION", "TRANSIT_BUS", "POLICE", "MAINTENANCE"
    latitude: float
    longitude: float
    speed_kmh: float
    heading_degrees: float
    fuel_level_percentage: float
    engine_rpm: float
    harsh_braking_detected: bool
    harsh_acceleration_detected: bool


class FleetTelematicsEngine:
    """Evaluates vehicle telematics, driver safety behavior, and fleet operational status."""
    def __init__(self, low_fuel_threshold_pct: float = 15.0):
        self.low_fuel_threshold = low_fuel_threshold_pct

    def evaluate_telematics(self, payload: VehicleTelemetryPayload) -> Dict[str, Any]:
        """Analyzes speed, fuel consumption, and aggressive driving safety infractions."""
        logger.info(f"Processing telemetry for vehicle {payload.vehicle_id} ({payload.fleet_type})...")

        safety_score = 100.0
        infractions = []

        if payload.harsh_braking_detected:
            safety_score -= 15.0
            infractions.append("HARSH_BRAKING")
            logger.warning(f"⚠️ Harsh braking detected for vehicle {payload.vehicle_id}!")

        if payload.harsh_acceleration_detected:
            safety_score -= 10.0
            infractions.append("HARSH_ACCELERATION")
            logger.warning(f"⚠️ Harsh acceleration detected for vehicle {payload.vehicle_id}!")

        if payload.speed_kmh > 120.0:
            safety_score -= 20.0
            infractions.append("SPEEDING_VIOLATION")
            logger.warning(f"🚨 Speeding violation for vehicle {payload.vehicle_id}: {payload.speed_kmh} km/h")

        low_fuel_warning = payload.fuel_level_percentage <= self.low_fuel_threshold
        operational_status = "NORMAL_OPERATION"

        if low_fuel_warning:
            operational_status = "LOW_FUEL_REFUEL_REQUIRED"
            logger.warning(f"⛽ Low fuel warning for vehicle {payload.vehicle_id}: {payload.fuel_level_percentage}%")

        report = {
            "vehicle_id": payload.vehicle_id,
            "fleet_type": payload.fleet_type,
            "coordinates": {"lat": payload.latitude, "lon": payload.longitude},
            "speed_kmh": payload.speed_kmh,
            "fuel_level_percentage": payload.fuel_level_percentage,
            "low_fuel_warning": low_fuel_warning,
            "driver_safety_score": max(0.0, safety_score),
            "infractions": infractions,
            "operational_status": operational_status,
            "timestamp": time.time()
        }
        return report


telematics_engine = FleetTelematicsEngine(low_fuel_threshold_pct=15.0)


@app.post("/api/v1/fleet/telematics/ingest", status_code=status.HTTP_200_OK)
def api_ingest_fleet_telematics(payload: VehicleTelemetryPayload):
    """API endpoint for municipal fleet units to broadcast live GPS coordinates and vehicle sensor telemetry."""
    try:
        report = telematics_engine.evaluate_telematics(payload)
        
        # Cache vehicle live state in Redis for real-time GIS command center mapping and spatial indexing
        cache_key = f"fleet:vehicle:{payload.vehicle_id}:telematics"
        redis_client.hset(cache_key, mapping={
            "lat": payload.latitude,
            "lon": payload.longitude,
            "speed": payload.speed_kmh,
            "fuel": payload.fuel_level_percentage,
            "status": report["operational_status"],
            "safety_score": report["driver_safety_score"],
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 300)  # Valid for 5 minutes

        return {
            "status": "success",
            "telematics_report": report
        }
    except Exception as e:
        logger.error(f"Fleet telematics processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fleet_telematics:app", host="0.0.0.0", port=8030, reload=True)
