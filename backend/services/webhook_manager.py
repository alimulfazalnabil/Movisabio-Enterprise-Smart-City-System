"""Standalone FastAPI service for signed webhook subscriptions and delivery."""

import os
import time
import hmac
import hashlib
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl
import httpx
import redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MoviSabio.WebhookManager")

app = FastAPI(
    title="MoviSabio Enterprise Webhook Notification & Orchestration Gateway",
    version="1.0.0",
    description="Manages event subscriptions, HMAC-signed payload dispatch, and asynchronous delivery orchestration."
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

WEBHOOK_SECRET = os.getenv("MOVISABIO_WEBHOOK_SECRET", "super_secret_webhook_hmac_key_2026")

class WebhookSubscription(BaseModel):
    """Target URL, event filter and optional signing secret."""

    subscriber_id: str
    target_url: str
    event_types: List[str]  # e.g., ["TRAFFIC_ALERT", "FLOOD_WARNING", "EMERGENCY_PREEMPTION"]
    secret_token: Optional[str] = None


class EventDispatchPayload(BaseModel):
    """Event name and data to send to matching subscriptions."""

    event_id: str
    event_type: str
    source_service: str
    payload_data: Dict[str, Any]


class WebhookManagerEngine:
    """Manages webhook subscriber registries and orchestrates secure event dispatch with HMAC signatures."""
    def __init__(self, default_secret: str):
        self.default_secret = default_secret

    def generate_hmac_signature(self, payload_bytes: bytes, secret: str) -> str:
        """Generates an HMAC-SHA256 signature for webhook payload authenticity verification."""
        signature = hmac.new(
            secret.encode('utf-8'),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"

    async def dispatch_webhook(self, target_url: str, event_payload: Dict[str, Any], secret: str) -> Dict[str, Any]:
        """Dispatches event telemetry to subscriber endpoint with async HTTP POST and signature header."""
        import json
        payload_json = json.dumps(event_payload)
        payload_bytes = payload_json.encode('utf-8')
        signature = self.generate_hmac_signature(payload_bytes, secret)

        headers = {
            "Content-Type": "application/json",
            "X-MoviSabio-Signature": signature,
            "X-MoviSabio-Event-ID": event_payload.get("event_id", "unknown")
        }

        logger.info(f"Dispatched webhook event {event_payload.get('event_type')} to {target_url}...")
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(target_url, content=payload_bytes, headers=headers)
                success = 200 <= response.status_code < 300
                return {
                    "target_url": target_url,
                    "status_code": response.status_code,
                    "delivered": success,
                    "timestamp": time.time()
                }
        except Exception as e:
            logger.error(f"Webhook delivery failed for {target_url}: {e}")
            return {
                "target_url": target_url,
                "status_code": 0,
                "delivered": False,
                "error": str(e),
                "timestamp": time.time()
            }


webhook_engine = WebhookManagerEngine(default_secret=WEBHOOK_SECRET)


@app.post("/api/v1/webhooks/subscribe", status_code=status.HTTP_201_CREATED)
def api_register_subscription(sub: WebhookSubscription):
    """API endpoint for municipal subsystems or external partners to register webhook event subscriptions."""
    try:
        cache_key = f"webhook:subscription:{sub.subscriber_id}"
        secret = sub.secret_token or WEBHOOK_SECRET
        
        redis_client.hset(cache_key, mapping={
            "subscriber_id": sub.subscriber_id,
            "target_url": sub.target_url,
            "event_types": ",".join(sub.event_types),
            "secret": secret,
            "registered_at": time.time()
        })

        return {
            "status": "success",
            "message": f"Webhook subscription registered successfully for {sub.subscriber_id}",
            "subscription": sub.model_dump()
        }
    except Exception as e:
        logger.error(f"Subscription registration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/webhooks/dispatch", status_code=status.HTTP_200_OK)
async def api_dispatch_event(event: EventDispatchPayload):
    """API endpoint to broadcast platform events to all matching registered webhook subscribers."""
    try:
        keys = redis_client.keys("webhook:subscription:*")
        dispatched_results = []

        event_dict = event.model_dump()

        for key in keys:
            sub_data = redis_client.hgetall(key)
            if not sub_data:
                continue

            event_types = sub_data.get("event_types", "").split(",")
            if event.event_type in event_types or "*" in event_types:
                target_url = sub_data.get("target_url")
                secret = sub_data.get("secret", WEBHOOK_SECRET)

                result = await webhook_engine.dispatch_webhook(target_url, event_dict, secret)
                dispatched_results.append(result)

        return {
            "status": "success",
            "event_id": event.event_id,
            "event_type": event.event_type,
            "deliveries": dispatched_results
        }
    except Exception as e:
        logger.error(f"Event dispatch orchestration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("webhook_manager:app", host="0.0.0.0", port=8034, reload=True)
