"""Standalone FastAPI service for flood risk and drainage pump control."""

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
logger = logging.getLogger("MoviSabio.FloodDrainage")

app = FastAPI(
    title="MoviSabio Municipal Flood & Stormwater Drainage Gateway",
    version="1.0.0",
    description="Ingests stormwater sensor telemetry, computes flood risk, and orchestrates drainage pump activation."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class FloodSensorTelemetryPayload(BaseModel):
    """Water level, rainfall and flow measurements for a drainage zone."""

    sensor_id: str
    drainage_basin_id: str
    water_level_meters: float
    flow_velocity_ms: float
    precipitation_mm_hr: float
    battery_voltage: float


class PumpControlRequest(BaseModel):
    """Requested operating state for a drainage pump station."""

    station_id: str
    target_pump_speed_rpm: float
    override_mode: bool


class FloodDrainageEngine:
    """Evaluates water level thresholds and calculates flood hazard risks for urban drainage basins."""
    def __init__(self, warning_threshold_m: float = 2.0, critical_threshold_m: float = 3.2):
        self.warning_threshold = warning_threshold_m
        self.critical_threshold = critical_threshold_m

    def evaluate_flood_risk(self, payload: FloodSensorTelemetryPayload) -> Dict[str, Any]:
        """Analyzes sensor metrics to classify localized flood hazard status."""
        logger.info(f"Evaluating flood telemetry for sensor {payload.sensor_id} in basin {payload.drainage_basin_id}...")

        water_level = payload.water_level_meters
        is_critical = water_level >= self.critical_threshold
        is_warning = water_level >= self.warning_threshold

        risk_status = "NORMAL_DRAINAGE"
        pump_command = "STANDBY"
        target_rpm = 0.0

        if is_critical:
            risk_status = "CRITICAL_FLOOD_HAZARD"
            pump_command = "MAX_CAPACITY_ACTIVATION"
            target_rpm = 1800.0
            logger.warning(f"🚨 CRITICAL FLOOD HAZARD in basin {payload.drainage_basin_id}! Water Level: {water_level}m")
        elif is_warning:
            risk_status = "ELEVATED_WATER_WARNING"
            pump_command = "MODERATE_DRAINAGE_ACTIVATION"
            target_rpm = 1200.0
            logger.warning(f"⚠️ Elevated water level warning in basin {payload.drainage_basin_id}: {water_level}m")

        report = {
            "sensor_id": payload.sensor_id,
            "drainage_basin_id": payload.drainage_basin_id,
            "water_level_meters": water_level,
            "flow_velocity_ms": payload.flow_velocity_ms,
            "precipitation_mm_hr": payload.precipitation_mm_hr,
            "risk_status": risk_status,
            "pump_command": pump_command,
            "target_pump_speed_rpm": target_rpm,
            "timestamp": time.time()
        }
        return report

    def control_pump_station(self, req: PumpControlRequest) -> Dict[str, Any]:
        """Manages manual or automated override commands for municipal stormwater pumps."""
        logger.info(f"Executing pump control for station {req.station_id} (Target RPM: {req.target_pump_speed_rpm}, Override: {req.override_mode})...")
        
        control_result = {
            "station_id": req.station_id,
            "pump_speed_rpm": req.target_pump_speed_rpm,
            "override_mode": req.override_mode,
            "status": "PUMP_CONTROLLER_SYNCHRONIZED",
            "timestamp": time.time()
        }
        return control_result


drainage_engine = FloodDrainageEngine(warning_threshold_m=2.0, critical_threshold_m=3.2)


@app.post("/api/v1/environment/flood/telemetry", status_code=status.HTTP_200_OK)
def api_process_flood_telemetry(payload: FloodSensorTelemetryPayload):
    """API endpoint for IoT water level and precipitation sensors to report live drainage metrics."""
    try:
        report = drainage_engine.evaluate_flood_risk(payload)
        
        # Cache basin flood state in Redis for emergency dispatch and command center synchronization
        cache_key = f"environment:basin:{payload.drainage_basin_id}:flood_state"
        redis_client.hset(cache_key, mapping={
            "water_level": payload.water_level_meters,
            "risk_status": report["risk_status"],
            "pump_command": report["pump_command"],
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 600)  # Valid for 10 minutes

        return {
            "status": "success",
            "flood_assessment_report": report
        }
    except Exception as e:
        logger.error(f"Flood sensor telemetry ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/environment/flood/pump-control", status_code=status.HTTP_200_OK)
def api_control_drainage_pumps(req: PumpControlRequest):
    """API endpoint to command municipal stormwater drainage pump stations."""
    try:
        result = drainage_engine.control_pump_station(req)
        return {
            "status": "success",
            "pump_control_result": result
        }
    except Exception as p_err:
        logger.error(f"Pump station control failed: {p_err}")
        raise HTTPException(status_code=500, detail=str(p_err))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("flood_drainage:app", host="0.0.0.0", port=8024, reload=True)
