from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class SafetyCheckResult(BaseModel):
    name: str
    result: str # 'PASS', 'FAIL'

class SafetyValidationResult(BaseModel):
    validation_id: str
    decision_id: str
    status: str # 'APPROVED', 'REJECTED'
    reason_code: Optional[str] = None
    checks: List[SafetyCheckResult]
    policy_version: str
    safety_version: str
    timestamp: datetime

class CommandAuthorization(BaseModel):
    authorization_id: str
    decision_id: str
    intersection_id: str
    controller_id: str
    
    action: Dict[str, Any]
    
    authorized_by: str = "safety-engine"
    policy_version: str
    safety_version: str
    
    expires_at: datetime
    status: str = "AUTHORIZED"
