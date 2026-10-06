from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone

class Entitlement(BaseModel):
    entitlement_id: str
    feature_code: str
    limit_type: str # BOOLEAN, QUANTITY
    limit_value: Optional[float] = None
    consumed_value: float = 0.0

class Subscription(BaseModel):
    subscription_id: str
    tenant_id: str
    plan_id: str
    status: str = "ACTIVE"
    entitlements: Dict[str, Entitlement] = {}
    
class EntitlementEngine:
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {} # tenant_id -> sub
        
    def add_subscription(self, sub: Subscription) -> None:
        self.subscriptions[sub.tenant_id] = sub
        
    def check_entitlement(self, tenant_id: str, feature_code: str, amount: float = 1.0) -> bool:
        """
        Check if the tenant has the entitlement and sufficient limits.
        """
        sub = self.subscriptions.get(tenant_id)
        if not sub or sub.status != "ACTIVE":
            return False
            
        ent = sub.entitlements.get(feature_code)
        if not ent:
            return False
            
        if ent.limit_type == "BOOLEAN":
            return True
            
        if ent.limit_type == "QUANTITY" and ent.limit_value is not None:
            if ent.consumed_value + amount <= ent.limit_value:
                return True
            return False
            
        return False
        
    def consume(self, tenant_id: str, feature_code: str, amount: float = 1.0) -> bool:
        if self.check_entitlement(tenant_id, feature_code, amount):
            self.subscriptions[tenant_id].entitlements[feature_code].consumed_value += amount
            return True
        return False
