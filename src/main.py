"""Compose the FastAPI gateway that is served by the main container."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from prometheus_client import make_asgi_app

from src.core.config import get_settings
from src.observability.middleware import ObservabilityMiddleware
from src.api.middleware.rate_limiter import RateLimitMiddleware
from src.api.middleware.idempotency import IdempotencyMiddleware
from src.api.exceptions import movisabio_exception_handler, validation_exception_handler, global_exception_handler, MoviSabioException
from src.api.v1.health import router as health_router

# Legacy Routers
from aitcs.presentation.api_router import router as aitcs_router
from aitcs.presentation.lane_detection_router import router as lane_detection_router
from aitcs.presentation.perception_router import router as perception_router

def create_unified_enterprise_platform() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="MoviSabio Enterprise API Gateway",
        description="Core API platform for traffic intelligence, IoT, and SaaS operations.",
        version="v1",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # 1. CORS Policy
    # In production, we restrict this based on allowed origins instead of "*"
    origins = ["*"] if settings.ENVIRONMENT != "production" else settings.FRONTEND_CORS_ORIGINS.split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Gateways & Observability Middlewares (Order matters: outermost first)
    app.add_middleware(IdempotencyMiddleware)
    app.add_middleware(RateLimitMiddleware, max_requests_per_minute=settings.API_RATE_LIMIT)
    app.add_middleware(ObservabilityMiddleware)

    # 3. Exception Handlers
    app.add_exception_handler(MoviSabioException, movisabio_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    # 4. Mount Prometheus Metrics
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    # 5. Core Platform API v1
    app.include_router(health_router, prefix="/api/v1")
    
    # 6. Legacy Mounts (To be sunset / migrated)
    app.include_router(aitcs_router)
    app.include_router(lane_detection_router)
    app.include_router(perception_router)

    return app

app = create_unified_enterprise_platform()
