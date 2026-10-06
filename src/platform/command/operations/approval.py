from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import enum

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    ESCALATED = "ESCALATED"

class ActionApproval(BaseModel):
    approval_id: str
    situation_id: str
    action_type: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    approver_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ApprovalEngine:
    def __init__(self):
        self.approvals: Dict[str, ActionApproval] = {}
        
    def request_approval(self, approval: ActionApproval) -> ActionApproval:
        self.approvals[approval.approval_id] = approval
        return approval
        
    def process_approval(self, approval_id: str, approver_id: str, decision: ApprovalStatus) -> ActionApproval:
        if approval_id not in self.approvals:
            raise ValueError("Approval not found")
        approval = self.approvals[approval_id]
        approval.approver_id = approver_id
        approval.status = decision
        return approval
