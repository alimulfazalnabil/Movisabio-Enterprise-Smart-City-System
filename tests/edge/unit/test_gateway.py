import pytest
from src.services.edge.models.schemas import EdgeDevice
from src.services.edge.engine.gateway import EdgeGateway

def test_gateway_device_auth():
    gateway = EdgeGateway()
    
    device = EdgeDevice(
        device_id="cam-001",
        node_id="edge-01",
        device_type="CAMERA",
        certificate_id="cert-cam-001",
        status="ACTIVE"
    )
    gateway.register_device(device)
    
    # Valid auth
    assert gateway.authenticate_payload("cam-001", "valid_sig_for_cert-cam-001", {"data": "video"}) is True
    
    # Invalid sig
    assert gateway.authenticate_payload("cam-001", "invalid_sig", {"data": "video"}) is False
    
    # Unknown device
    assert gateway.authenticate_payload("cam-999", "sig", {}) is False
