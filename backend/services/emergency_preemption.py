"""Standalone FastAPI service for emergency-vehicle signal preemption."""

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
logger = logging.getLogger("MoviSabio.EmergencyPreemption")

app = FastAPI(
    title="MoviSabio Automated Emergency Vehicle Preemption Gateway",
    version="1.0.0",
    description="Ingests emergency vehicle GPS beacons and triggers intersection green wave preemption protocols."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class EmergencyBeaconPayload(BaseModel):
    """Live position and motion data broadcast by an emergency vehicle."""

    vehicle_id: str
    vehicle_type: str  # e.g., "FIRE_ENGINE", "AMBULANCE", "POLICE"
    latitude: float
    longitude: float
    speed_kmh: float
    heading_degrees: float
    target_intersection_id: str


class EmergencyPreemptionEngine:
    """Calculates emergency vehicle ETAs and manages intersection traffic signal preemption."""
    def __init__(self, preemption_distance_threshold_m: float = 500.0):
        self.preemption_threshold_m = preemption_distance_threshold_m

    def calculate_preemption(self, payload: EmergencyBeaconPayload, intersection_lat: float, intersection_lon: float) -> Dict[str, Any]:
        """Computes distance, ETA, and triggers green wave signal preemption."""
        logger.info(f"Processing emergency beacon for {payload.vehicle_type} ({payload.vehicle_id}) approaching {payload.target_intersection_id}...")

        # Simplified Haversine distance proxy in meters
        lat_diff = payload.latitude - intersection_lat
        lon_diff = payload.longitude - intersection_lon
        distance_m = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111000.0  # rough conversion degrees to meters

        speed_ms = max(0.5, payload.speed_kmh * (1000.0 / 3600.0))
        eta_seconds = distance_m / speed_ms

        trigger_preemption = distance_m <= self.preemption_threshold_m

        action_status = "MONITORING_APPROACH"
        if trigger_preemption:
            action_status = "INTERSECTION_GREEN_WAVE_ACTIVE"
            logger.warning(f"🚨 EMERGENCY PREEMPTION TRIGGERED at intersection {payload.target_intersection_id} for {payload.vehicle_id}! ETA: {round(eta_seconds, 1)}s")

        report = {
            "vehicle_id": payload.vehicle_id,
            "vehicle_type": payload.vehicle_type,
            "target_intersection_id": payload.target_intersection_id,
            "distance_meters": round(distance_m, 1),
            "eta_seconds": round(eta_seconds, 1),
            "preemption_active": trigger_preemption,
            "signal_state": "FORCED_GREEN" if trigger_preemption else "NORMAL_OPERATION",
            "timestamp": time.time()
        }
        return report


preemption_engine = EmergencyPreemptionEngine()


@app.post("/api/v1/emergency/beacon", status_code=status.HTTP_200_OK)
def api_process_emergency_beacon(payload: EmergencyBeaconPayload):
    """API endpoint for emergency vehicle transponders to broadcast live GPS coordinates and request preemption."""
    try:
        # Retrieve intersection coordinates from Redis cache or mock default
        intersection_key = f"intersection:{payload.target_intersection_id}:coords"
        cached_coords = redis_client.hgetall(intersection_key)
        
        inter_lat = float(cached_coords.get("lat", payload.latitude + 0.002))
        inter_lon = float(cached_coords.get("lon", payload.longitude + 0.002))

        report = preemption_engine.calculate_preemption(payload, inter_lat, inter_lon)

        # Cache preemption state in Redis for traffic light controller synchronization
        cache_key = f"preemption:intersection:{payload.target_intersection_id}"
        if report["preemption_active"]:
            redis_client.hset(cache_key, mapping={
                "active": "True",
                "vehicle_id": payload.vehicle_id,
                "vehicle_type": payload.vehicle_type,
                "eta": report["eta_seconds"],
                "timestamp": report["timestamp"]
            })
            redis_client.expire(cache_key, 60)  # Short expiration for active emergency windows
        else:
            redis_client.delete(cache_key)

        return {
            "status": "success",
            "preemption_report": report
        }
    except Exception as e:
        logger.error(f"Emergency preemption processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("emergency_preemption:app", host="0.0.0.0", port=8021, reload=True)
