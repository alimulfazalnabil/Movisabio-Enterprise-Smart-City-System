from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class Identity(BaseModel):
    identity_id: str
    identity_type: str # HUMAN, ORGANIZATION, DEVICE, AI_AGENT
    status: str # VERIFIED, ACTIVE, SUSPENDED, REVOKED
    attributes: Dict[str, str]

class DataAsset(BaseModel):
    asset_id: str
    owner: str
    classification: str # PUBLIC, INTERNAL, RESTRICTED, CONFIDENTIAL, PERSONAL
    jurisdiction: str

class AccessRequest(BaseModel):
    subject_id: str
    resource_id: str
    action: str
    purpose: str

class DataTransferRequest(BaseModel):
    asset_id: str
    source_jurisdiction: str
    target_jurisdiction: str

class TrustDecision(BaseModel):
    decision: str # ALLOW, DENY, REVIEW_REQUIRED
    reason: Optional[str] = None
