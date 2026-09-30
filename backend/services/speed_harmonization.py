"""Standalone FastAPI service for variable speed-limit recommendations."""

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
logger = logging.getLogger("MoviSabio.SpeedHarmonization")

app = FastAPI(
    title="MoviSabio V2I Speed Harmonization & VSL Gateway",
    version="1.0.0",
    description="Computes and broadcasts Variable Speed Limits (VSL) via V2I to mitigate traffic shockwaves."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class SpeedHarmonizationPayload(BaseModel):
    """Road-segment density and speed data used to recommend a limit."""

    segment_id: str
    current_average_speed_kmh: float
    traffic_density_veh_km: float
    downstream_queue_length_m: float
    weather_visibility_meters: float


class SpeedHarmonizationEngine:
    """Evaluates highway density and downstream congestion to compute optimal variable speed limits."""
    def __init__(self, base_speed_limit_kmh: float = 100.0, critical_density_veh_km: float = 35.0, min_speed_limit_kmh: float = 40.0):
        self.base_speed = base_speed_limit_kmh
        self.critical_density = critical_density_veh_km
        self.min_speed = min_speed_limit_kmh

    def compute_variable_speed_limit(self, payload: SpeedHarmonizationPayload) -> Dict[str, Any]:
        """Calculates recommended VSL based on traffic density and downstream queue hazard."""
        logger.info(f"Computing VSL for corridor segment {payload.segment_id} (Density: {payload.traffic_density_veh_km} veh/km)...")

        # Weather visibility penalty check
        visibility_factor = 1.0
        if payload.weather_visibility_meters < 200.0:
            visibility_factor = 0.7  # Severe reduction for heavy fog or heavy rain
            logger.warning(f"⚠️ Low visibility advisory in segment {payload.segment_id}: {payload.weather_visibility_meters}m")

        # Density-based VSL step-down algorithm
        vsl_target = self.base_speed
        if payload.traffic_density_veh_km > self.critical_density:
            excess_density = payload.traffic_density_veh_km - self.critical_density
            reduction_factor = max(0.0, 1.0 - (excess_density * 0.02))
            vsl_target = max(self.min_speed, self.base_speed * reduction_factor)

        # Downstream queue congestion override
        if payload.downstream_queue_length_m > 300.0:
            vsl_target = min(vsl_target, 50.0)
            logger.warning(f"🛑 Downstream congestion queue detected ({payload.downstream_queue_length_m}m). Enforcing strict VSL cap.")

        # Apply visibility multiplier
        final_vsl = max(self.min_speed, round(vsl_target * visibility_factor, -1))  # Round to nearest 10 km/h

        harmonization_report = {
            "segment_id": payload.segment_id,
            "baseline_speed_limit_kmh": self.base_speed,
            "recommended_vsl_kmh": int(final_vsl),
            "traffic_density_veh_km": payload.traffic_density_veh_km,
            "downstream_queue_m": payload.downstream_queue_length_m,
            "harmonization_active": int(final_vsl) < self.base_speed,
            "timestamp": time.time()
        }
        return harmonization_report


harmonization_engine = SpeedHarmonizationEngine(base_speed_limit_kmh=100.0, critical_density_veh_km=35.0)


@app.post("/api/v1/traffic/speed-harmonization", status_code=status.HTTP_200_OK)
def api_compute_speed_harmonization(payload: SpeedHarmonizationPayload):
    """API endpoint to ingest corridor sensor metrics and output dynamic VSL recommendations."""
    try:
        report = harmonization_engine.compute_variable_speed_limit(payload)
        
        # Cache active VSL state in Redis for roadside Dynamic Message Signs (DMS) and connected vehicle broadcasts
        cache_key = f"traffic:segment:{payload.segment_id}:vsl"
        redis_client.hset(cache_key, mapping={
            "vsl_kmh": report["recommended_vsl_kmh"],
            "active": str(report["harmonization_active"]),
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 300)  # Valid for 5 minutes

        return {
            "status": "success",
            "harmonization_report": report
        }
    except Exception as e:
        logger.error(f"Speed harmonization calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("speed_harmonization:app", host="0.0.0.0", port=8022, reload=True)
