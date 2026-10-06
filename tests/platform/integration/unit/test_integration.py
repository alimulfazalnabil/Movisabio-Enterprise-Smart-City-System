import pytest
from datetime import datetime, timezone
from src.platform.integration.gateway.api import APIGateway, RateLimiter, RequestContext
from src.platform.integration.webhooks.dispatcher import WebhookDispatcher

def test_api_gateway_rate_limit():
    limiter = RateLimiter()
    gateway = APIGateway(limiter)
    
    ctx = RequestContext(
        request_id="req-1",
        tenant_id="tenant-1",
        partner_id="partner-1",
        identity_id="id-1",
        scopes=["traffic.read"],
        timestamp=datetime.now(timezone.utc)
    )
    
    # PUBLIC limit is 100, we'll set it to 1 for testing
    limiter.limits["PUBLIC"] = 1
    
    # First request should pass
    resp1 = gateway.handle_request(ctx, "traffic.read", "PUBLIC")
    assert "data" in resp1
    
    # Second request should fail rate limit
    ctx.request_id = "req-2"
    resp2 = gateway.handle_request(ctx, "traffic.read", "PUBLIC")
    assert "error" in resp2
    assert resp2["error"]["code"] == "RATE_LIMIT_EXCEEDED"

def test_api_gateway_scope():
    limiter = RateLimiter()
    gateway = APIGateway(limiter)
    
    ctx = RequestContext(
        request_id="req-1",
        tenant_id="tenant-1",
        partner_id="partner-1",
        identity_id="id-1",
        scopes=["traffic.read"],
        timestamp=datetime.now(timezone.utc)
    )
    
    # Require a scope they don't have
    resp = gateway.handle_request(ctx, "traffic.control")
    assert "error" in resp
    assert resp["error"]["code"] == "INSUFFICIENT_SCOPE"

def test_webhook_signature():
    payload = {"event": "traffic.incident", "id": "inc-1"}
    secret = "my-secret-key"
    timestamp = "2026-10-06T01:10:00Z"
    
    headers = WebhookDispatcher.prepare_webhook_headers(payload, secret, "evt-1", timestamp)
    
    assert headers["Content-Type"] == "application/json"
    assert headers["X-MoviSabio-Event-ID"] == "evt-1"
    assert headers["X-MoviSabio-Timestamp"] == timestamp
    assert "X-MoviSabio-Signature" in headers
    
    # Verify the signature component starts correctly
    assert headers["X-MoviSabio-Signature"].startswith(f"t={timestamp},v1=")
