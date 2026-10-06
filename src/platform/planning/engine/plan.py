from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import enum

class PlanStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ASSESSMENT = "ASSESSMENT"
    DESIGNING = "DESIGNING"
    SIMULATION = "SIMULATION"
    REVIEW = "REVIEW"
    POLICY_EVALUATION = "POLICY_EVALUATION"
    APPROVAL_PENDING = "APPROVAL_PENDING"
    APPROVED = "APPROVED"
    IMPLEMENTING = "IMPLEMENTING"
    MONITORING = "MONITORING"
    EVALUATING = "EVALUATING"
    ADAPTING = "ADAPTING"
    COMPLETED = "COMPLETED"

class PlanType(str, enum.Enum):
    STRATEGIC = "STRATEGIC"
    TACTICAL = "TACTICAL"
    OPERATIONAL = "OPERATIONAL"
    REAL_TIME = "REAL_TIME"

class Plan(BaseModel):
    plan_id: str
    tenant_id: str
    twin_id: str
    name: str
    plan_type: PlanType
    status: PlanStatus = PlanStatus.DRAFT
    objectives: List[Dict[str, Any]]
    interventions: List[str] = []
    kpis: List[Dict[str, Any]] = []
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class PlanningEngine:
    def __init__(self):
        self.plans: Dict[str, Plan] = {}
        
    def create_plan(self, plan: Plan) -> Plan:
        self.plans[plan.plan_id] = plan
        return plan
        
    def transition_state(self, plan_id: str, new_status: PlanStatus) -> Plan:
        if plan_id not in self.plans:
            raise ValueError("Plan not found")
        self.plans[plan_id].status = new_status
        return self.plans[plan_id]
