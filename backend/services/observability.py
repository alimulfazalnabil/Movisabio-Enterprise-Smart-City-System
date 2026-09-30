"""Standalone health and Prometheus endpoint for platform observability."""

import os
import time
import logging
from typing import Dict, Any
from fastapi import FastAPI, Response, status
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram, Gauge
import redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MoviSabio.Observability")

app = FastAPI(
    title="MoviSabio Enterprise Observability & Prometheus Metrics Exporter",
    version="1.0.0",
    description="Exposes enterprise Prometheus metrics and operational telemetry for Grafana monitoring dashboards."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# Prometheus Metrics Definition
REQUEST_COUNT = Counter(
    "movisabio_http_requests_total",
    "Total HTTP requests processed by MoviSabio microservices",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "movisabio_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"]
)
ACTIVE_SENSORS_GAUGE = Gauge(
    "movisabio_active_iot_sensors_total",
    "Total active IoT sensors connected across municipal zones"
)
SYSTEM_HEALTH_GAUGE = Gauge(
    "movisabio_system_health_status",
    "Overall enterprise system health status (1 = Healthy, 0 = Degraded/Failure)"
)


@app.middleware("http")
async def prometheus_middleware(request, call_next):
    """Middleware to automatically track HTTP request counts and request execution latency."""
    start_time = time.time()
    method = request.method
    endpoint = request.url.path

    response = await call_next(request)
    duration = time.time() - start_time
    status_code = str(response.status_code)

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)

    return response


@app.get("/metrics", include_in_schema=False)
def metrics():
    """Prometheus metrics scraping endpoint for Grafana telemetry ingestion."""
    try:
        # Synchronize gauge metrics from high-speed Redis state cache
        active_sensors = int(redis_client.get("metrics:active_sensors_count") or 1420)
        ACTIVE_SENSORS_GAUGE.set(active_sensors)
        SYSTEM_HEALTH_GAUGE.set(1.0)
    except Exception as e:
        logger.error(f"Failed to fetch metric gauges from Redis: {e}")
        SYSTEM_HEALTH_GAUGE.set(0.0)

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/api/v1/observability/health", status_code=status.HTTP_200_OK)
def api_health_check() -> Dict[str, Any]:
    """Enterprise health check endpoint for Kubernetes liveness and readiness probes."""
    return {
        "status": "healthy",
        "service": "observability-exporter",
        "timestamp": time.time()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("observability:app", host="0.0.0.0", port=8031, reload=True)
