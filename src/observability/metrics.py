from prometheus_client import Counter, Histogram, Gauge

# API RED Metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code", "tenant_id"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint", "tenant_id"],
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# AI / ML Operational Metrics
model_inference_latency = Histogram(
    "model_inference_latency_seconds",
    "Latency of AI model inferences",
    ["model_name", "model_version", "tenant_id"]
)

model_inference_errors = Counter(
    "model_inference_errors_total",
    "Total errors during model inference",
    ["model_name", "model_version", "tenant_id"]
)

# Traffic Control Metrics
traffic_command_latency = Histogram(
    "traffic_command_latency_seconds",
    "Latency to receive acknowledgement from traffic controller",
    ["controller_id", "tenant_id"]
)

traffic_commands_total = Counter(
    "traffic_commands_total",
    "Total traffic control commands issued",
    ["controller_id", "tenant_id", "status"] # status: success, failed, timeout
)

active_controllers_gauge = Gauge(
    "active_controllers",
    "Number of currently online traffic controllers",
    ["tenant_id"]
)
