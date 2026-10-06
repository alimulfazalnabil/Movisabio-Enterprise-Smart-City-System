from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class Subscription(BaseModel):
    subscription_id: str
    tenant_id: str
    product_id: str
    active: bool = True
    entitlements: Dict[str, float]  # e.g., {"api_calls": 10000}
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SubscriptionManager:
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {}
        
    def create_subscription(self, sub: Subscription) -> Subscription:
        self.subscriptions[sub.subscription_id] = sub
        return sub
        
    def check_entitlement(self, subscription_id: str, metric: str, amount: float = 1.0) -> bool:
        if subscription_id not in self.subscriptions:
            return False
        sub = self.subscriptions[subscription_id]
        if not sub.active:
            return False
        allocated = sub.entitlements.get(metric, 0)
        return allocated >= amount
