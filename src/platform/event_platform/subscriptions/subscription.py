from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class EventSubscription(BaseModel):
    subscription_id: str
    application_id: str
    event_types: List[str]
    geography: Optional[str] = None
    minimum_severity: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SubscriptionManager:
    def __init__(self):
        self.subscriptions: Dict[str, EventSubscription] = {}
        
    def register_subscription(self, sub: EventSubscription) -> EventSubscription:
        self.subscriptions[sub.subscription_id] = sub
        return sub
        
    def get_subscriptions_for_event(self, event_type: str) -> List[EventSubscription]:
        return [sub for sub in self.subscriptions.values() if event_type in sub.event_types]
