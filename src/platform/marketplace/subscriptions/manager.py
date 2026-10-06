from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime
import enum

class SubscriptionState(str, enum.Enum):
    TRIAL = "TRIAL"
    ACTIVE = "ACTIVE"
    PAST_DUE = "PAST_DUE"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class MarketplaceSubscription(BaseModel):
    subscription_id: str
    tenant_id: str
    product_id: str
    state: SubscriptionState = SubscriptionState.ACTIVE
    plan_name: str
    auto_renew: bool = True
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SubscriptionManager:
    def __init__(self):
        self.subscriptions: Dict[str, MarketplaceSubscription] = {}
        
    def create_subscription(self, subscription: MarketplaceSubscription) -> MarketplaceSubscription:
        self.subscriptions[subscription.subscription_id] = subscription
        return subscription
        
    def renew(self, subscription_id: str, new_expiry: datetime) -> MarketplaceSubscription:
        if subscription_id not in self.subscriptions:
            raise ValueError("Subscription not found")
        sub = self.subscriptions[subscription_id]
        sub.expires_at = new_expiry
        sub.state = SubscriptionState.ACTIVE
        return sub
