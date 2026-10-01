import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_gateway_404_error():
    response = client.get("/api/v1/invalid-route-does-not-exist")
    assert response.status_code == 404
    # The default FastAPI 404 returns {"detail": "Not Found"}
    # But since we have a global exception handler, it might be overridden if we specifically catch 404s.
    # We only catch RequestValidationError and Exception currently, not Starlette HTTPExceptions.
    # But we can at least assert the Gateway is routing.
    
def test_gateway_health_endpoints():
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    
    response = client.get("/api/v1/health/startup")
    assert response.status_code == 200
    
def test_gateway_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
