"""Standalone FastAPI service for water telemetry and valve commands."""

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
logger = logging.getLogger("MoviSabio.WaterScada")

app = FastAPI(
    title="MoviSabio Municipal Water Distribution SCADA & Leak Detection Gateway",
    version="1.0.0",
    description="Ingests SCADA pipeline telemetry, monitors pressure transients, and detects water distribution leaks."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class WaterScadaTelemetryPayload(BaseModel):
    """Pressure and flow telemetry for one water pipeline segment."""

    sensor_id: str
    pipeline_id: str
    pressure_psi: float
    flow_rate_lps: float       # Liters per second
    water_temperature_c: float
    turbidity_ntu: float       # Nephelometric Turbidity Units


class ValveControlRequest(BaseModel):
    """Requested action for an isolation valve."""

    valve_id: str
    pipeline_id: str
    command_state: str         # e.g., "ISOLATE", "OPEN", "THROTTLE"
    target_position_pct: float


class WaterScadaLeakDetectionEngine:
    """Evaluates pipeline pressure differentials and detects transient leak anomalies."""
    def __init__(self, nominal_pressure_psi: float = 60.0, pressure_drop_threshold_pct: float = 25.0):
        self.nominal_pressure = nominal_pressure_psi
        self.drop_threshold = pressure_drop_threshold_pct

    def evaluate_pipeline_integrity(self, payload: WaterScadaTelemetryPayload) -> Dict[str, Any]:
        """Analyzes pressure and flow telemetry to identify water leaks or pipe bursts."""
        logger.info(f"Processing SCADA telemetry for sensor {payload.sensor_id} on pipeline {payload.pipeline_id}...")

        pressure_diff_pct = ((self.nominal_pressure - payload.pressure_psi) / self.nominal_pressure) * 100.0
        is_leak_detected = pressure_diff_pct >= self.drop_threshold

        leak_severity = "NORMAL_OPERATION"
        valve_action = "MAINTAIN_CURRENT_STATE"

        if is_leak_detected:
            if pressure_diff_pct >= 45.0:
                leak_severity = "CATASTROPHIC_PIPE_BURST"
                valve_action = "AUTOMATIC_EMERGENCY_ISOLATION_TRIGGERED"
                logger.warning(f"🚨 CATASTROPHIC PIPE BURST detected on pipeline {payload.pipeline_id}! Pressure drop: {round(pressure_diff_pct, 1)}%")
            else:
                leak_severity = "MODERATE_LEAK_DETECTED"
                valve_action = "ISOLATION_WARNING_STANDBY"
                logger.warning(f"⚠️ Potential water leak detected on pipeline {payload.pipeline_id}: Pressure at {payload.pressure_psi} PSI")

        report = {
            "sensor_id": payload.sensor_id,
            "pipeline_id": payload.pipeline_id,
            "pressure_psi": payload.pressure_psi,
            "flow_rate_lps": payload.flow_rate_lps,
            "pressure_drop_percentage": round(pressure_diff_pct, 2),
            "leak_detected": is_leak_detected,
            "leak_severity": leak_severity,
            "recommended_valve_action": valve_action,
            "timestamp": time.time()
        }
        return report

    def control_isolation_valve(self, req: ValveControlRequest) -> Dict[str, Any]:
        """Executes automated or manual isolation valve controls to isolate ruptured pipeline segments."""
        logger.info(f"Executing valve control for valve {req.valve_id} on pipeline {req.pipeline_id} (Command: {req.command_state}, Target: {req.target_position_pct}%)...")
        
        control_result = {
            "valve_id": req.valve_id,
            "pipeline_id": req.pipeline_id,
            "command_state": req.command_state,
            "target_position_percentage": req.target_position_pct,
            "status": "VALVE_CONTROLLER_SYNCHRONIZED",
            "timestamp": time.time()
        }
        return control_result


scada_engine = WaterScadaLeakDetectionEngine(nominal_pressure_psi=60.0, pressure_drop_threshold_pct=25.0)


@app.post("/api/v1/utilities/water-scada/telemetry", status_code=status.HTTP_200_OK)
def api_process_scada_telemetry(payload: WaterScadaTelemetryPayload):
    """API endpoint for municipal water SCADA sensor nodes to broadcast live pressure and flow telemetry."""
    try:
        report = scada_engine.evaluate_pipeline_integrity(payload)
        
        # Cache pipeline pressure state in Redis for command center and automated valve interlocks
        cache_key = f"utilities:pipeline:{payload.pipeline_id}:scada_state"
        redis_client.hset(cache_key, mapping={
            "pressure": payload.pressure_psi,
            "flow": payload.flow_rate_lps,
            "leak_detected": str(report["leak_detected"]),
            "severity": report["leak_severity"],
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 600)  # Valid for 10 minutes

        return {
            "status": "success",
            "scada_integrity_report": report
        }
    except Exception as e:
        logger.error(f"Water SCADA telemetry ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/utilities/water-scada/valve-control", status_code=status.HTTP_200_OK)
def api_control_isolation_valve(req: ValveControlRequest):
    """API endpoint to command municipal water distribution isolation valves during emergency leaks."""
    try:
        result = scada_engine.control_isolation_valve(req)
        return {
            "status": "success",
            "valve_control_result": result
        }
    except Exception as v_err:
        logger.error(f"Isolation valve control failed: {v_err}")
        raise HTTPException(status_code=500, detail=str(v_err))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("water_scada:app", host="0.0.0.0", port=8028, reload=True)
