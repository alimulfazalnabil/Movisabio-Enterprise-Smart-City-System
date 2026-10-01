import hmac
import hashlib
import time

def generate_webhook_signature(secret: str, payload_body: str, timestamp: str) -> str:
    """
    Generates a secure HMAC-SHA256 signature for outgoing webhooks.
    """
    canonical_payload = f"{timestamp}.{payload_body}"
    
    signature = hmac.new(
        secret.encode('utf-8'),
        canonical_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature

def verify_webhook_signature(secret: str, payload_body: str, timestamp: str, signature: str, tolerance_seconds: int = 300) -> bool:
    """
    Verifies an incoming webhook signature securely.
    """
    try:
        ts = int(timestamp)
    except ValueError:
        return False
        
    now = int(time.time())
    if abs(now - ts) > tolerance_seconds:
        # Reject expired/replay attacks
        return False
        
    expected_signature = generate_webhook_signature(secret, payload_body, timestamp)
    
    return hmac.compare_digest(expected_signature, signature)
