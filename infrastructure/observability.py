from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI

def setup_observability(app: FastAPI):
    """
    Phase 8: Observability
    Deploy OpenTelemetry tracing for the FastAPI app.
    Monitors: AI inference latency, API availability, Decision latency.
    """
    # Set up global tracer provider
    provider = TracerProvider()
    
    # Configure OTLP Exporter (e.g. Jaeger or Tempo)
    otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)
    
    trace.set_tracer_provider(provider)
    
    # Instrument the FastAPI app
    FastAPIInstrumentor.instrument_app(app)
    
    print("OpenTelemetry observability configured successfully.")
