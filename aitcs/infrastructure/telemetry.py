"""Prometheus metric collectors shared by AITCS request and decision paths."""

from prometheus_client import Counter, Histogram, Gauge

TRAFFIC_TELEMETRY_INGESTED = Counter(
    "aitcs_telemetry_ingested_total",
    "Total number of raw edge telemetry packets ingested",
    ["intersection_id"]
)

SIGNAL_DECISION_LATENCY = Histogram(
    "aitcs_decision_latency_seconds",
    "Latency of the AI decision and safety validation loop",
    ["intersection_id"]
)

ACTIVE_CONGESTION_GAUGE = Gauge(
    "aitcs_active_congestion_index",
    "Current normalized congestion index per intersection",
    ["intersection_id"]
)
