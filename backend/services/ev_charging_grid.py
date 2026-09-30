"""Standalone FastAPI service for EV charging demand response."""

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
logger = logging.getLogger("MoviSabio.EVChargingGrid")

app = FastAPI(
    title="MoviSabio Smart Grid & EV Charging Demand Response Gateway",
    version="1.0.0",
    description="Orchestrates EV charging power throttling and dynamic pricing during grid peak stress events."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class EVStationTelemetryPayload(BaseModel):
    """Capacity and power draw reported by one charging station."""

    station_id: str
    grid_zone_id: str
    active_charging_slots: int
    total_power_demand_kw: float
    grid_capacity_kw: float
    current_electricity_price_kwh: float


class DemandResponseOptimizationRequest(BaseModel):
    """Zone-wide load and reduction target for demand response."""

    grid_zone_id: str
    target_load_reduction_kw: float
    response_window_minutes: int


class EVChargingDemandResponseEngine:
    """Evaluates grid stress ratios and computes dynamic power throttling and tariff surge responses."""
    def __init__(self, stress_threshold_ratio: float = 0.85, base_tariff_kwh: float = 0.15):
        self.stress_threshold = stress_threshold_ratio
        self.base_tariff = base_tariff_kwh

    def evaluate_grid_stress(self, payload: EVStationTelemetryPayload) -> Dict[str, Any]:
        """Analyzes substation capacity utilization and calculates dynamic demand response actions."""
        logger.info(f"Evaluating grid stress for station {payload.station_id} in zone {payload.grid_zone_id}...")

        stress_ratio = payload.total_power_demand_kw / max(1.0, payload.grid_capacity_kw)
        grid_stressed = stress_ratio >= self.stress_threshold

        action_mode = "NORMAL_OPERATION"
        throttle_percentage = 100.0
        adjusted_tariff = self.base_tariff

        if grid_stressed:
            action_mode = "DEMAND_RESPONSE_THROTTLING_ACTIVE"
            excess_ratio = stress_ratio - self.stress_threshold
            # Throttle power output down proportionally to mitigate substation overload
            throttle_percentage = max(40.0, 100.0 - (excess_ratio * 150.0))
            # Surge electricity tariff to discourage non-essential fast charging during peak hours
            adjusted_tariff = round(self.base_tariff * (1.0 + (excess_ratio * 3.0)), 4)
            logger.warning(f"⚡ GRID STRESS ALERT in zone {payload.grid_zone_id}! Capacity Utilization: {round(stress_ratio * 100.0, 1)}%. Throttling charging slots to {round(throttle_percentage, 1)}%.")

        report = {
            "station_id": payload.station_id,
            "grid_zone_id": payload.grid_zone_id,
            "capacity_utilization_percentage": round(stress_ratio * 100.0, 2),
            "grid_stressed": grid_stressed,
            "action_mode": action_mode,
            "allowed_power_throttle_percentage": round(throttle_percentage, 1),
            "adjusted_tariff_kwh": adjusted_tariff,
            "timestamp": time.time()
        }
        return report

    def optimize_zone_demand_response(self, req: DemandResponseOptimizationRequest) -> Dict[str, Any]:
        """Calculates multi-station load shedding requirements across a municipal grid zone."""
        logger.info(f"Orchestrating zone-wide demand response for {req.grid_zone_id} (Target Reduction: {req.target_load_reduction_kw} kW)...")
        
        # Simulated distribution of load shedding across connected EV chargers in the zone
        distributed_reduction = req.target_load_reduction_kw * 0.25

        response_plan = {
            "grid_zone_id": req.grid_zone_id,
            "target_reduction_kw": req.target_load_reduction_kw,
            "response_window_minutes": req.response_window_minutes,
            "command_dispatched": "ECO_THROTTLE_AND_PRICE_SURGE",
            "estimated_shed_capacity_kw": round(req.target_load_reduction_kw * 0.95, 2),
            "timestamp": time.time()
        }
        return response_plan


ev_engine = EVChargingDemandResponseEngine(stress_threshold_ratio=0.85, base_tariff_kwh=0.15)


@app.post("/api/v1/energy/ev-station/telemetry", status_code=status.HTTP_200_OK)
def api_process_ev_telemetry(payload: EVStationTelemetryPayload):
    """API endpoint for municipal EV charging hubs to broadcast live power draw and receive DR commands."""
    try:
        report = ev_engine.evaluate_grid_stress(payload)
        
        # Cache active grid station throttling state in Redis for fast charger controller synchronization
        cache_key = f"energy:station:{payload.station_id}:dr_state"
        redis_client.hset(cache_key, mapping={
            "action_mode": report["action_mode"],
            "throttle_pct": report["allowed_power_throttle_percentage"],
            "tariff": report["adjusted_tariff_kwh"],
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 600)  # Valid for 10 minutes

        return {
            "status": "success",
            "demand_response_report": report
        }
    except Exception as e:
        logger.error(f"EV telemetry processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/energy/demand-response/orchestrate", status_code=status.HTTP_200_OK)
def api_orchestrate_zone_dr(req: DemandResponseOptimizationRequest):
    """API endpoint to trigger automated grid-wide load reduction protocols across municipal subgrids."""
    try:
        plan = ev_engine.optimize_zone_demand_response(req)
        return {
            "status": "success",
            "demand_response_plan": plan
        }
    except Exception as g_err:
        logger.error(f"Demand response orchestration failed: {g_err}")
        raise HTTPException(status_code=500, detail=str(g_err))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ev_charging_grid:app", host="0.0.0.0", port=8023, reload=True)
