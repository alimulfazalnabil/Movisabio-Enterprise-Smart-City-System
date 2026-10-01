import pytest
import time
from src.api.webhooks.signatures import generate_webhook_signature, verify_webhook_signature

def test_webhook_signature_generation_and_verification():
    secret = "whsec_test_secret_12345"
    payload = '{"event": "traffic.optimization.completed", "data": {"intersection": "042"}}'
    timestamp = str(int(time.time()))
    
    signature = generate_webhook_signature(secret, payload, timestamp)
    
    assert signature is not None
    assert len(signature) == 64 # SHA256 length
    
    # Verify success
    assert verify_webhook_signature(secret, payload, timestamp, signature) is True
    
    # Verify failure on tampered payload
    assert verify_webhook_signature(secret, payload + " ", timestamp, signature) is False
    
    # Verify failure on tampered signature
    assert verify_webhook_signature(secret, payload, timestamp, "bad_signature") is False

def test_webhook_signature_expiration():
    secret = "whsec_test_secret_12345"
    payload = '{"event": "ping"}'
    
    # 10 minutes ago
    old_timestamp = str(int(time.time()) - 600)
    signature = generate_webhook_signature(secret, payload, old_timestamp)
    
    # With default 300s tolerance, this should fail
    assert verify_webhook_signature(secret, payload, old_timestamp, signature) is False
    
    # If we artificially increase tolerance to 1000s, it should pass
    assert verify_webhook_signature(secret, payload, old_timestamp, signature, tolerance_seconds=1000) is True
