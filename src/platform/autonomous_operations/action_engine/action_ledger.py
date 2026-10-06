from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class AutonomyLevel(int, enum.Enum):
    L0_OBSERVE = 0
    L1_DETECT = 1
    L2_RECOMMEND = 2
    L3_AUTOMATE_LOW_RISK = 3
    L4_CONDITIONAL_AUTONOMY = 4
    L5_HIGH_IMPACT = 5

class ActionStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    BLOCKED = "BLOCKED"
    APPROVED = "APPROVED"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"

class AutonomousAction(BaseModel):
    action_id: str
    agent_id: str
    action_type: str
    autonomy_level: AutonomyLevel
    budget_cost: float = 0.0
    status: ActionStatus = ActionStatus.PROPOSED
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ActionLedger:
    def __init__(self, agent_budget: float = 1000.0):
        self.actions: Dict[str, AutonomousAction] = {}
        self.remaining_budget = agent_budget
        self.kill_switch_active = False
        
    def propose_action(self, action: AutonomousAction) -> AutonomousAction:
        if self.kill_switch_active:
            action.status = ActionStatus.BLOCKED
            self.actions[action.action_id] = action
            return action
            
        # Enforce Autonomy Boundaries
        if action.autonomy_level >= AutonomyLevel.L5_HIGH_IMPACT:
            # L5 requires explicit human approval, so we just log it as PROPOSED
            action.status = ActionStatus.PROPOSED
        elif action.budget_cost > self.remaining_budget:
            action.status = ActionStatus.BLOCKED
        else:
            # L3 and L4 can execute if budget allows
            action.status = ActionStatus.EXECUTED
            self.remaining_budget -= action.budget_cost
            
        self.actions[action.action_id] = action
        return action
        
    def activate_kill_switch(self):
        self.kill_switch_active = True
