import hmac
import hashlib
import json
from typing import Dict, Any

class WebhookDispatcher:
    @staticmethod
    def generate_signature(payload: Dict[str, Any], secret: str, timestamp: str) -> str:
        """
        Generates HMAC-SHA256 signature for webhook payload to prevent forgery.
        """
        message = f"{timestamp}.{json.dumps(payload, sort_keys=True)}"
        return hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def prepare_webhook_headers(payload: Dict[str, Any], secret: str, event_id: str, timestamp: str) -> Dict[str, str]:
        """
        Prepares standard security headers for outgoing webhooks.
        """
        signature = WebhookDispatcher.generate_signature(payload, secret, timestamp)
        return {
            "Content-Type": "application/json",
            "X-MoviSabio-Event-ID": event_id,
            "X-MoviSabio-Timestamp": timestamp,
            "X-MoviSabio-Signature": f"t={timestamp},v1={signature}"
        }
