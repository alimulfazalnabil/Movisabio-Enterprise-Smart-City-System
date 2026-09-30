"""Standalone FastAPI service for Redis-backed drone-nest dispatch."""

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
logger = logging.getLogger("MoviSabio.DroneDispatch")

app = FastAPI(
    title="MoviSabio Automated Drone-in-a-Box Emergency Reconnaissance Gateway",
    version="1.0.0",
    description="Dispatches automated reconnaissance drones to emergency incident sites and manages aerial telemetry."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class IncidentDispatchPayload(BaseModel):
    """Incident location and conditions used to select a drone nest."""

    incident_id: str
    incident_type: str  # e.g., "TRAFFIC_ACCIDENT", "PIPE_BURST", "FLOOD_HAZARD", "FIRE_OUTBREAK"
    latitude: float
    longitude: float
    priority_level: int  # 1 to 5


class DroneNestStatusPayload(BaseModel):
    """Availability, location and battery status for one drone nest."""

    nest_id: str
    latitude: float
    longitude: float
    drone_available: bool
    battery_percentage: float
    weather_wind_speed_ms: float


class DroneDispatchEngine:
    """Calculates optimal drone nest dispatch vectors and manages autonomous aerial reconnaissance missions."""
    def __init__(self, max_wind_speed_ms: float = 15.0, min_battery_pct: float = 30.0):
        self.max_wind_speed = max_wind_speed_ms
        self.min_battery = min_battery_pct

    def select_optimal_drone_nest(self, incident_lat: float, incident_lon: float, available_nests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluates distance, battery status, and weather conditions to select the best drone nest."""
        logger.info("Evaluating available drone-in-a-box nests for emergency dispatch...")

        best_nest = None
        min_distance = float('inf')

        for nest in available_nests:
            if not nest.get("drone_available", False):
                continue
            if nest.get("battery_percentage", 0.0) < self.min_battery:
                continue
            if nest.get("weather_wind_speed_ms", 0.0) > self.max_wind_speed:
                continue

            # Haversine distance proxy in meters
            lat_diff = incident_lat - nest["latitude"]
            lon_diff = incident_lon - nest["longitude"]
            distance_m = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111000.0

            if distance_m < min_distance:
                min_distance = distance_m
                best_nest = nest

        if not best_nest:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No viable drone nests available (weather constraints, low battery, or fleet busy)."
            )

        # Estimate flight time assuming average drone transit speed of 15 m/s (~54 km/h)
        drone_speed_ms = 15.0
        flight_time_seconds = min_distance / drone_speed_ms

        mission_profile = {
            "selected_nest_id": best_nest["nest_id"],
            "nest_coordinates": {"lat": best_nest["latitude"], "lon": best_nest["longitude"]},
            "estimated_distance_meters": round(min_distance, 1),
            "estimated_flight_time_seconds": round(flight_time_seconds, 1),
            "mission_status": "AUTONOMOUS_LAUNCH_DISPATCHED",
            "timestamp": time.time()
        }
        return mission_profile


drone_engine = DroneDispatchEngine()


@app.post("/api/v1/emergency/drone/dispatch", status_code=status.HTTP_200_OK)
def api_dispatch_reconnaissance_drone(payload: IncidentDispatchPayload):
    """API endpoint to trigger automated drone-in-a-box deployment for live emergency reconnaissance."""
    try:
        # Retrieve active municipal drone nests from Redis cache or mock registry
        nests_keys = redis_client.keys("drone:nest:*:status")
        available_nests = []

        if nests_keys:
            for k in nests_keys:
                data = redis_client.hgetall(k)
                if data:
                    available_nests.append({
                        "nest_id": data.get("nest_id"),
                        "latitude": float(data.get("lat", 0.0)),
                        "longitude": float(data.get("lon", 0.0)),
                        "drone_available": data.get("available") == "True",
                        "battery_percentage": float(data.get("battery", 100.0)),
                        "weather_wind_speed_ms": float(data.get("wind_speed", 5.0))
                    })
        else:
            # Fallback mock active nest if none registered in Redis yet
            available_nests = [{
                "nest_id": "NEST-CENTRAL-01",
                "latitude": payload.latitude - 0.01,
                "longitude": payload.longitude - 0.01,
                "drone_available": True,
                "battery_percentage": 95.0,
                "weather_wind_speed_ms": 4.2
            }]

        mission = drone_engine.select_optimal_drone_nest(payload.latitude, payload.longitude, available_nests)
        mission["incident_id"] = payload.incident_id
        mission["incident_type"] = payload.incident_type

        # Cache active mission state in Redis for command center video feed integration
        cache_key = f"emergency:drone:mission:{payload.incident_id}"
        redis_client.hset(cache_key, mapping={
            "nest_id": mission["selected_nest_id"],
            "status": mission["mission_status"],
            "eta_seconds": mission["estimated_flight_time_seconds"],
            "timestamp": mission["timestamp"]
        })
        redis_client.expire(cache_key, 1800)  # Valid for 30 minutes

        return {
            "status": "success",
            "drone_dispatch_mission": mission
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Drone reconnaissance dispatch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("drone_dispatch:app", host="0.0.0.0", port=8032, reload=True)
