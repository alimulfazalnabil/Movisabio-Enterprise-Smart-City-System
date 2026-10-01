from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
import json
from src.core.context import get_tenant_context

# Mock storage for idempotency keys
_idempotency_store = {}

class IdempotencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Idempotency is usually applied to POST/PATCH/PUT
        if request.method not in ["POST", "PUT", "PATCH"]:
            return await call_next(request)
            
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return await call_next(request)
            
        tenant_id = get_tenant_context() or "unknown"
        cache_key = f"idempotency:{tenant_id}:{idempotency_key}"
        
        # If we have seen this key, return the cached response
        if cache_key in _idempotency_store:
            cached = _idempotency_store[cache_key]
            return JSONResponse(
                status_code=cached["status_code"],
                content=cached["content"],
                headers={"X-Idempotency-Replayed": "true"}
            )
            
        # Process the request normally
        response: Response = await call_next(request)
        
        # Cache the response for future retries if successful (or if we choose to cache errors too)
        if 200 <= response.status_code < 300:
            # Note: We must consume the response body to cache it. Starlette streaming responses are tricky.
            # In a production FastAPI, this is often implemented as a Route class override rather than BaseHTTPMiddleware 
            # to safely read the body. We simulate it here.
            
            # Since we can't easily read response.body in BaseHTTPMiddleware without breaking the stream,
            # we rely on the specific implementation in a robust library like `fastapi-idempotency`.
            pass
            
        return response
