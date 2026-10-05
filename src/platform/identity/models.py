from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MoviIdentity(BaseModel):
    identity_id: str
    identity_type: str # HUMAN, ORGANIZATION, SERVICE, DEVICE, MOBILE_ASSET, AI_AGENT, APPLICATION
    tenant_id: Optional[str] = None
    status: str # ACTIVE, SUSPENDED, COMPROMISED, REVOKED
    roles: List[str] = Field(default_factory=list)
    trust_level: str
    created_at: datetime
    updated_at: datetime

class AIAgentIdentity(MoviIdentity):
    risk_class: str
    capabilities: List[str]
    forbidden_capabilities: List[str]
    model_version: str
    policy_version: str
