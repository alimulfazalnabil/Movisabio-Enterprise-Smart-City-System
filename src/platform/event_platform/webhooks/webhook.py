from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class WebhookStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    SUSPENDED = "SUSPENDED"

class Webhook(BaseModel):
    webhook_id: str
    application_id: str
    endpoint_url: str
    status: WebhookStatus = WebhookStatus.SUBMITTED
    secret: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WebhookManager:
    def __init__(self):
        self.webhooks: Dict[str, Webhook] = {}
        
    def register_webhook(self, webhook: Webhook) -> Webhook:
        self.webhooks[webhook.webhook_id] = webhook
        return webhook
        
    def activate_webhook(self, webhook_id: str) -> Webhook:
        if webhook_id not in self.webhooks:
            raise ValueError("Webhook not found")
        self.webhooks[webhook_id].status = WebhookStatus.ACTIVE
        return self.webhooks[webhook_id]
