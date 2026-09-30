"""Standalone FastAPI service for air-quality telemetry and eco-routing."""

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
logger = logging.getLogger("MoviSabio.AirQualityRouting")

app = FastAPI(
    title="MoviSabio Municipal Air Quality & Eco-Routing Gateway",
    version="1.0.0",
    description="Monitors IoT air quality sensor telemetry and computes low-emission eco-routing paths."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class AirQualityTelemetryPayload(BaseModel):
    """Pollutant and weather measurements reported for one zone."""

    station_id: str
    zone_id: str
    pm25_ug_m3: float  # Particulate Matter 2.5 (µg/m³)
    no2_ppb: float     # Nitrogen Dioxide (ppb)
    co2_ppm: float     # Carbon Dioxide (ppm)
    temperature_c: float
    humidity_percentage: float
    latitude: float
    longitude: float


class EcoRouteRequest(BaseModel):
    """Candidate route data used to balance travel and pollution exposure."""

    route_id: str
    origin_zone: str
    destination_zone: str
    baseline_distance_km: float
    baseline_duration_minutes: float
    corridor_zone_ids: List[str]


class AirQualityRoutingEngine:
    """Evaluates atmospheric pollution indices and computes weighted eco-routing costs."""
    def __init__(self, pm25_limit: float = 35.0, no2_limit: float = 100.0):
        self.pm25_limit = pm25_limit
        self.no2_limit = no2_limit

    def evaluate_air_quality(self, payload: AirQualityTelemetryPayload) -> Dict[str, Any]:
        """Analyzes pollutant metrics to classify localized air quality health hazards."""
        logger.info(f"Evaluating air quality telemetry for station {payload.station_id} in zone {payload.zone_id}...")

        # Air Quality Index (AQI) proxy calculation based on PM2.5 and NO2
        hazardous_condition = (payload.pm25_ug_m3 >= self.pm25_limit) or (payload.no2_ppb >= self.no2_limit)
        
        aqi_status = "GOOD"
        if hazardous_condition:
            aqi_status = "UNHEALTHY_HIGH_POLLUTION"
            logger.warning(f"⚠️ HIGH POLLUTION ALERT in zone {payload.zone_id}! PM2.5: {payload.pm25_ug_m3} µg/m³, NO2: {payload.no2_ppb} ppb")
        elif payload.pm25_ug_m3 >= (self.pm25_limit * 0.7):
            aqi_status = "MODERATE_SENSITIVE_WARNING"

        report = {
            "station_id": payload.station_id,
            "zone_id": payload.zone_id,
            "pm25_ug_m3": payload.pm25_ug_m3,
            "no2_ppb": payload.no2_ppb,
            "co2_ppm": payload.co2_ppm,
            "aqi_status": aqi_status,
            "hazardous_flag": hazardous_condition,
            "coordinates": {"lat": payload.latitude, "lon": payload.longitude},
            "timestamp": time.time()
        }
        return report

    def optimize_eco_route(self, req: EcoRouteRequest) -> Dict[str, Any]:
        """Calculates eco-routing cost penalty based on real-time pollutant telemetry cached in Redis."""
        total_pollution_penalty = 0.0
        
        for zone in req.corridor_zone_ids:
            cached_status = redis_client.hgetall(f"environment:zone:{zone}:air_quality")
            if cached_status and cached_status.get("hazardous_flag") == "True":
                total_pollution_penalty += 1.5  # Heavy penalty for routing through polluted zones

        # Eco-routing cost function balancing distance, time, and emission exposure
        alpha, beta, gamma = 1.0, 0.8, 2.5
        eco_cost_score = (alpha * req.baseline_distance_km) + (beta * req.baseline_duration_minutes) + (gamma * total_pollution_penalty)

        recommendation = {
            "route_id": req.route_id,
            "baseline_distance_km": req.baseline_distance_km,
            "baseline_duration_minutes": req.baseline_duration_minutes,
            "pollution_penalty_factor": total_pollution_penalty,
            "eco_cost_score": round(eco_cost_score, 2),
            "reroute_recommended": total_pollution_penalty > 0.0,
            "timestamp": time.time()
        }
        return recommendation


air_quality_engine = AirQualityRoutingEngine()


@app.post("/api/v1/environment/air-quality/telemetry", status_code=status.HTTP_200_OK)
def api_process_air_quality_telemetry(payload: AirQualityTelemetryPayload):
    """API endpoint for IoT air quality sensor nodes to report live pollutant metrics."""
    try:
        report = air_quality_engine.evaluate_air_quality(payload)
        
        # Cache zone air quality state in Redis for routing optimization engines
        cache_key = f"environment:zone:{payload.zone_id}:air_quality"
        redis_client.hset(cache_key, mapping={
            "pm25": payload.pm25_ug_m3,
            "no2": payload.no2_ppb,
            "status": report["aqi_status"],
            "hazardous_flag": str(report["hazardous_flag"]),
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 1800)  # Valid for 30 minutes

        return {
            "status": "success",
            "air_quality_report": report
        }
    except Exception as e:
        logger.error(f"Air quality telemetry ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/environment/eco-route/optimize", status_code=status.HTTP_200_OK)
def api_optimize_eco_route(req: EcoRouteRequest):
    """API endpoint to compute low-emission eco-routing recommendations avoiding polluted corridors."""
    try:
        optimization_result = air_quality_engine.optimize_eco_route(req)
        return {
            "status": "success",
            "eco_routing_result": optimization_result
        }
    except Exception as e:
        logger.error(f"Eco-route optimization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("air_quality_routing:app", host="0.0.0.0", port=8020, reload=True)
