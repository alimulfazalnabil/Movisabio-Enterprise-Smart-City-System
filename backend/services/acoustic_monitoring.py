"""Standalone FastAPI service for acoustic thresholds and siren events."""

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
    format="%(asctime)s [%(levelname)s] %(name: %(message)s"
)
logger = logging.getLogger("MoviSabio.AcousticMonitoring")

app = FastAPI(
    title="MoviSabio Municipal Acoustic Noise Pollution & Siren Detection Gateway",
    version="1.0.0",
    description="Ingests roadside acoustic telemetry, monitors noise pollution limits, and detects emergency sirens."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class AcousticTelemetryPayload(BaseModel):
    """Noise level and audio classifications reported by one sensor."""

    sensor_id: str
    zone_id: str
    decibel_level_db: float
    peak_frequency_hz: float
    siren_signature_detected: bool
    ambient_noise_profile: str  # e.g., "HEAVY_TRAFFIC", "CONSTRUCTION", "QUIET"


class AcousticMonitoringEngine:
    """Evaluates noise pollution thresholds and processes emergency siren audio signatures."""
    def __init__(self, daytime_noise_limit_db: float = 65.0, nighttime_noise_limit_db: float = 55.0):
        self.day_limit = daytime_noise_limit_db
        self.night_limit = nighttime_noise_limit_db

    def evaluate_acoustic_telemetry(self, payload: AcousticTelemetryPayload) -> Dict[str, Any]:
        """Analyzes decibel levels and detects emergency siren audio triggers."""
        logger.info(f"Processing acoustic telemetry for sensor {payload.sensor_id} in zone {payload.zone_id}...")

        # Determine noise violation status (assuming daytime threshold for operational check)
        is_noise_violation = payload.decibel_level_db >= self.day_limit
        violation_severity = "NORMAL"

        if is_noise_violation:
            excess_db = payload.decibel_level_db - self.day_limit
            if excess_db >= 15.0:
                violation_severity = "SEVERE_NOISE_POLLUTION"
                logger.warning(f"🔊 SEVERE NOISE POLLUTION in zone {payload.zone_id}: {payload.decibel_level_db} dB!")
            else:
                violation_severity = "MODERATE_NOISE_EXCEEDANCE"
                logger.warning(f"⚠️ Noise limit exceeded in zone {payload.zone_id}: {payload.decibel_level_db} dB")

        siren_status = "NO_SIREN_DETECTED"
        if payload.siren_signature_detected:
            siren_status = "EMERGENCY_SIREN_CONFIRMED"
            logger.warning(f"🚨 EMERGENCY SIREN SIGNATURE DETECTED in zone {payload.zone_id} at {payload.peak_frequency_hz} Hz!")

        report = {
            "sensor_id": payload.sensor_id,
            "zone_id": payload.zone_id,
            "decibel_level_db": payload.decibel_level_db,
            "noise_violation": is_noise_violation,
            "violation_severity": violation_severity,
            "siren_status": siren_status,
            "peak_frequency_hz": payload.peak_frequency_hz,
            "timestamp": time.time()
        }
        return report


acoustic_engine = AcousticMonitoringEngine(daytime_noise_limit_db=65.0, nighttime_noise_limit_db=55.0)


@app.post("/api/v1/environment/acoustic/telemetry", status_code=status.HTTP_200_OK)
def api_process_acoustic_telemetry(payload: AcousticTelemetryPayload):
    """API endpoint for roadside acoustic sensor arrays to report live decibel metrics and siren triggers."""
    try:
        report = acoustic_engine.evaluate_acoustic_telemetry(payload)
        
        # Cache zone acoustic state in Redis for command center and emergency preemption synchronization
        cache_key = f"environment:zone:{payload.zone_id}:acoustic"
        redis_client.hset(cache_key, mapping={
            "decibel_level": payload.decibel_level_db,
            "violation": str(report["noise_violation"]),
            "siren_detected": str(payload.siren_signature_detected),
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 300)  # Valid for 5 minutes

        return {
            "status": "success",
            "acoustic_assessment_report": report
        }
    except Exception as e:
        logger.error(f"Acoustic telemetry processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("acoustic_monitoring:app", host="0.0.0.0", port=8026, reload=True)
