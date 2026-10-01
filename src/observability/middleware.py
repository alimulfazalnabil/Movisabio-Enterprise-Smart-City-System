import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.core.context import set_trace_context, get_tenant_context
from src.observability.metrics import http_requests_total, http_request_duration_seconds
from src.observability.logger import get_logger

logger = get_logger()

class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        
        # 1. Extract or Generate Trace IDs
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        correlation_id = request.headers.get("X-Correlation-ID", request_id)
        
        # 2. Inject into ContextVars (Async safe)
        set_trace_context(request_id, correlation_id)
        
        # 3. Process Request
        response = None
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error("unhandled_request_exception", extra_attrs={"error": str(e)})
            raise e
        finally:
            # 4. Measure Metrics
            duration = time.time() - start_time
            status_code = response.status_code if response else 500
            
            # The tenant_id will only be present if authentication dependency was evaluated successfully
            tenant_id = get_tenant_context() or "unknown"
            
            # Record RED metrics
            http_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=str(status_code),
                tenant_id=tenant_id
            ).inc()
            
            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.url.path,
                tenant_id=tenant_id
            ).observe(duration)
            
            # Add trace ID headers to the outbound response
            if response:
                response.headers["X-Request-ID"] = request_id
                response.headers["X-Correlation-ID"] = correlation_id
