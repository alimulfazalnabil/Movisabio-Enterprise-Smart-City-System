import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.api.middleware.idempotency import IdempotencyMiddleware
from src.core.context import set_tenant_context

app = FastAPI()
app.add_middleware(IdempotencyMiddleware)

@app.post("/test")
async def post_test():
    return {"status": "created"}
    
client = TestClient(app)

def test_idempotency_middleware_passthrough_no_header():
    set_tenant_context("tenant_123")
    response = client.post("/test")
    assert response.status_code == 200

# In a real implementation test with fastapi-idempotency, we'd verify the header caching behavior
