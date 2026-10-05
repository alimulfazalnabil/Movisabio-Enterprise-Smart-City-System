from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from src.platform.identity.models import MoviIdentity

class AccessRequest(BaseModel):
    subject: MoviIdentity
    action: str
    resource_id: str
    resource_type: str
    tenant_id: str
    purpose: str
    context: dict = Field(default_factory=dict)

class AuthorizationDecision(BaseModel):
    decision: str # ALLOW, DENY, STEP_UP, HUMAN_APPROVAL
    subject_id: str
    action: str
    resource_id: str
    tenant_id: str
    risk_class: Optional[str] = None
    conditions: List[str] = Field(default_factory=list)
    policy_version: str
    expires_at: Optional[datetime] = None
