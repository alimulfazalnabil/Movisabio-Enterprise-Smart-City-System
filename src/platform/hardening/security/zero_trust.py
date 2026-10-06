from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class AccessResult(str, enum.Enum):
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    CHALLENGED = "CHALLENGED"

class AccessRequest(BaseModel):
    request_id: str
    who: str
    what_resource: str
    why: str
    where_from: str
    when: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    under_policy: str
    risk_level: str

class ZeroTrustEnforcer:
    def __init__(self):
        self.blocked_ips: set = set()
        self.required_policies: set = set()
        
    def require_policy(self, policy_id: str):
        self.required_policies.add(policy_id)
        
    def evaluate(self, req: AccessRequest) -> AccessResult:
        if req.where_from in self.blocked_ips:
            return AccessResult.DENIED
            
        if req.under_policy not in self.required_policies:
            return AccessResult.DENIED
            
        if req.risk_level == "HIGH":
            return AccessResult.CHALLENGED
            
        return AccessResult.GRANTED
