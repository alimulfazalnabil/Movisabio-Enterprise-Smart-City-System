from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class CommandEnvelope(BaseModel):
    command_id: str
    target_type: str
    target_id: str
    command_type: str
    
    requested_by: str
    
    policy_version: str
    safety_policy_version: str
    
    idempotency_key: str
    expires_at: datetime
    
    authorization: Dict[str, Any] = Field(default_factory=dict)
    payload: Dict[str, Any] = Field(default_factory=dict)
