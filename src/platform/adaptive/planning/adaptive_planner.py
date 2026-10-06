from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class PlanStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ADAPTING = "ADAPTING"
    ADAPTED = "ADAPTED"
    BLOCKED = "BLOCKED"

class ExecutionPlan(BaseModel):
    plan_id: str
    target_date: datetime
    budget: float
    resources_needed: int
    status: PlanStatus = PlanStatus.ACTIVE
    adaptation_history: List[str] = Field(default_factory=list)

class AdaptivePlanner:
    def __init__(self):
        self.plans: Dict[str, ExecutionPlan] = {}
        
    def register_plan(self, plan: ExecutionPlan) -> ExecutionPlan:
        self.plans[plan.plan_id] = plan
        return plan
        
    def adapt_plan(self, plan_id: str, trigger_situation: str, budget_change: float, schedule_delay_days: int) -> ExecutionPlan:
        if plan_id not in self.plans:
            raise ValueError("Plan not found")
            
        plan = self.plans[plan_id]
        plan.status = PlanStatus.ADAPTING
        
        plan.budget += budget_change
        
        # In a real system we'd use timedelta, simplifying for mock
        import datetime as dt
        plan.target_date = plan.target_date + dt.timedelta(days=schedule_delay_days)
        
        plan.adaptation_history.append(f"Adapted due to {trigger_situation}. Budget changed by {budget_change}. Delayed {schedule_delay_days} days.")
        plan.status = PlanStatus.ADAPTED
        
        return plan
