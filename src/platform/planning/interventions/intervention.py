from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import enum

class InterventionStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    ANALYZED = "ANALYZED"
    SIMULATED = "SIMULATED"
    RISK_ASSESSED = "RISK_ASSESSED"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    IMPLEMENTING = "IMPLEMENTING"
    ACTIVE = "ACTIVE"
    EVALUATING = "EVALUATING"
    COMPLETED = "COMPLETED"

class Intervention(BaseModel):
    intervention_id: str
    plan_id: str
    type: str
    status: InterventionStatus = InterventionStatus.PROPOSED
    expected_outcomes: Dict[str, float]
    actual_outcomes: Dict[str, float] = {}
