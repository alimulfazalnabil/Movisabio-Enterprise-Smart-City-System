from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import time
from src.core.context import get_tenant_context, get_trace_context

# In a real environment, this utilizes Redis (e.g. redis-py + Token Bucket).
# Here we mock the structural dependency to satisfy the API boundary.

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests_per_minute: int = 100):
        super().__init__(app)
        self.max_requests_per_minute = max_requests_per_minute
        # Mock storage for testing
        self._request_counts = {}

    async def dispatch(self, request: Request, call_next):
        # Apply limits based on tenant or IP
        tenant_id = get_tenant_context() or request.client.host
        
        current_time = int(time.time() // 60)
        key = f"rate_limit:{tenant_id}:{current_time}"
        
        count = self._request_counts.get(key, 0)
        
        if count >= self.max_requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "TOO_MANY_REQUESTS",
                        "message": "Rate limit exceeded. Please retry later.",
                        "request_id": get_trace_context().get("request_id")
                    }
                },
                headers={"Retry-After": "60"}
            )
            
        self._request_counts[key] = count + 1
        
        # Cleanup mock
        if len(self._request_counts) > 1000:
            self._request_counts.clear()
            
        return await call_next(request)
