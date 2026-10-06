from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone

class ApprovalRequest(BaseModel):
    request_id: str
    tenant_id: str
    requester_id: str
    action_type: str
    target_resource: str
    risk_level: str # LOW, MEDIUM, HIGH, CRITICAL
    evidence: str
    status: str = "PENDING" # PENDING, APPROVED, REJECTED
    created_at: datetime
    
class ApprovalCenter:
    def __init__(self):
        self.requests: Dict[str, ApprovalRequest] = {}
        
    def submit_request(self, req: ApprovalRequest) -> None:
        self.requests[req.request_id] = req
        
    def resolve_request(self, request_id: str, approver_id: str, decision: str) -> bool:
        req = self.requests.get(request_id)
        if not req or req.status != "PENDING":
            return False
            
        req.status = decision
        return True
