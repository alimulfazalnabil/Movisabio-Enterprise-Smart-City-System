import pytest
import time
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.middleware.rate_limiter import RateLimitMiddleware
from src.core.context import set_tenant_context

app = FastAPI()
# Strict limit of 2 req/min for testing
app.add_middleware(RateLimitMiddleware, max_requests_per_minute=2)

@app.get("/test")
async def get_test():
    return {"status": "ok"}
    
client = TestClient(app)

def test_rate_limiting_enforcement():
    set_tenant_context("tenant_rl")
    
    # Request 1
    resp1 = client.get("/test")
    assert resp1.status_code == 200
    
    # Request 2
    resp2 = client.get("/test")
    assert resp2.status_code == 200
    
    # Request 3 should be blocked
    resp3 = client.get("/test")
    assert resp3.status_code == 429
    assert resp3.headers["Retry-After"] == "60"
    
    data = resp3.json()
    assert "error" in data
    assert data["error"]["code"] == "TOO_MANY_REQUESTS"
