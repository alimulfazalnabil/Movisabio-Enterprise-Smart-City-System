from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class GovernmentOrganization(BaseModel):
    org_id: str
    name: str
    level: str # MUNICIPALITY, DEPARTMENT, DIVISION, UNIT
    parent_id: Optional[str] = None

class GovernmentCase(BaseModel):
    case_id: str
    case_type: str
    status: str # SUBMITTED, UNDER_REVIEW, APPROVED, REJECTED, CLOSED
    assigned_department: str
    created_at: datetime
    resolution: Optional[str] = None

class SpatialPolicy(BaseModel):
    policy_id: str
    jurisdiction: str
    rule_type: str
    constraints: Dict[str, str]

class PermitApplication(BaseModel):
    permit_id: str
    applicant_id: str
    permit_type: str
    location: str
    status: str
    compliance_status: Optional[str] = None # COMPLIANT, NON_COMPLIANT, REQUIRES_REVIEW
