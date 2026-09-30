"""Standalone FastAPI service for region health and traffic routing."""

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
logger = logging.getLogger("MoviSabio.GlobalTrafficManager")

app = FastAPI(
    title="MoviSabio Multi-Region Global Traffic Manager & Failover Gateway",
    version="1.0.0",
    description="Monitors multi-region Kubernetes cluster health and orchestrates dynamic GTM traffic routing."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

class RegionHealthPayload(BaseModel):
    """Availability, latency and capacity reported by one service region."""

    region_id: str
    cluster_endpoint: str
    status_healthy: bool
    latency_ms: float
    cpu_utilization_percentage: float
    error_rate_percentage: float
    active_ingress_connections: int


class GTMRoutingRequest(BaseModel):
    """Client region and candidate destinations for global routing."""

    client_region: str
    available_regions: List[str]


class GlobalTrafficManagerEngine:
    """Evaluates multi-region cluster health metrics and computes optimized traffic weighting and failover routing."""
    def __init__(self, max_latency_ms: float = 250.0, max_error_rate_pct: float = 2.0):
        self.max_latency = max_latency_ms
        self.max_error_rate = max_error_rate_pct

    def evaluate_region_health(self, payload: RegionHealthPayload) -> Dict[str, Any]:
        """Analyzes regional cluster telemetry to determine health scores and operational viability."""
        logger.info(f"Evaluating health telemetry for region {payload.region_id} ({payload.cluster_endpoint})...")

        is_viable = (
            payload.status_healthy and
            payload.latency_ms <= self.max_latency and
            payload.error_rate_percentage <= self.max_error_rate
        )

        health_status = "HEALTHY_OPTIMAL"
        if not is_viable:
            health_status = "DEGRADED_FAILOVER_TRIGGERED"
            logger.warning(f"⚠️ REGION DEGRADED/FAILED in {payload.region_id}! Latency: {payload.latency_ms}ms, Error Rate: {payload.error_rate_percentage}%")

        report = {
            "region_id": payload.region_id,
            "cluster_endpoint": payload.cluster_endpoint,
            "health_status": health_status,
            "viable_for_routing": is_viable,
            "latency_ms": payload.latency_ms,
            "error_rate_percentage": payload.error_rate_percentage,
            "cpu_utilization_percentage": payload.cpu_utilization_percentage,
            "timestamp": time.time()
        }
        return report

    def compute_gtm_routing(self, req: GTMRoutingRequest) -> Dict[str, Any]:
        """Calculates latency and capacity-weighted routing weights across all available regions."""
        logger.info(f"Computing GTM routing table for client region {req.client_region} across regions: {req.available_regions}...")

        region_weights = {}
        viable_regions = []

        for region in req.available_regions:
            cached_health = redis_client.hgetall(f"gtm:region:{region}:health")
            if cached_health and cached_health.get("viable_for_routing") == "True":
                viable_regions.append(region)
                lat = float(cached_health.get("latency_ms", 50.0))
                err = float(cached_health.get("error_rate_percentage", 0.1))
                
                # Inverse penalty scoring for traffic weighting
                score = max(1.0, 1000.0 / (lat + (err * 100.0)))
                region_weights[region] = score
            else:
                region_weights[region] = 0.0  # Zero weight for failed regions

        # Normalize weights to percentages
        total_score = sum(region_weights.values())
        routing_percentages = {}
        if total_score > 0:
            for reg, score in region_weights.items():
                routing_percentages[reg] = round((score / total_score) * 100.0, 2)
        else:
            # Fallback emergency routing if all tracked primary regions fail
            routing_percentages[req.available_regions[0]] = 100.0
            logger.error("🚨 CRITICAL: All primary GTM regions degraded. Routing traffic to fallback anchor region.")

        selected_primary_region = max(routing_percentages, key=routing_percentages.get)

        routing_decision = {
            "client_region": req.client_region,
            "selected_primary_region": selected_primary_region,
            "region_traffic_distribution_pct": routing_percentages,
            "failover_active": len(viable_regions) < len(req.available_regions),
            "timestamp": time.time()
        }
        return routing_decision


gtm_engine = GlobalTrafficManagerEngine(max_latency_ms=250.0, max_error_rate_pct=2.0)


@app.post("/api/v1/gtm/region/health", status_code=status.HTTP_200_OK)
def api_report_region_health(payload: RegionHealthPayload):
    """API endpoint for Kubernetes clusters across regions to report live health telemetry."""
    try:
        report = gtm_engine.evaluate_region_health(payload)
        
        # Cache region health state in Redis for GTM DNS router synchronization
        cache_key = f"gtm:region:{payload.region_id}:health"
        redis_client.hset(cache_key, mapping={
            "status": report["health_status"],
            "viable_for_routing": str(report["viable_for_routing"]),
            "latency_ms": payload.latency_ms,
            "error_rate": payload.error_rate_percentage,
            "timestamp": report["timestamp"]
        })
        redis_client.expire(cache_key, 60)  # Valid for 60 seconds

        return {
            "status": "success",
            "region_health_report": report
        }
    except Exception as e:
        logger.error(f"Region health reporting failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/gtm/route/resolve", status_code=status.HTTP_200_OK)
def api_resolve_gtm_routing(req: GTMRoutingRequest):
    """API endpoint to resolve optimal multi-region traffic routing weights and failover targets."""
    try:
        decision = gtm_engine.compute_gtm_routing(req)
        return {
            "status": "success",
            "gtm_routing_decision": decision
        }
    except Exception as g_err:
        logger.error(f"GTM routing resolution failed: {g_err}")
        raise HTTPException(status_code=500, detail=str(g_err))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("global_traffic_manager:app", host="0.0.0.0", port=8025, reload=True)
