import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from src.core.config import get_settings

settings = get_settings()

def setup_telemetry():
    if not settings.OTEL_ENDPOINT:
        logging.getLogger("movisabio").info("OTEL_ENDPOINT not set. Telemetry disabled.")
        return
        
    resource = Resource(attributes={
        "service.name": settings.APP_NAME,
        "service.version": settings.APP_VERSION,
        "environment": settings.APP_ENV
    })
    
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=settings.OTEL_ENDPOINT, insecure=True)
    processor = BatchSpanProcessor(exporter)
    
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    
    logging.getLogger("movisabio").info("OpenTelemetry configured successfully.")
