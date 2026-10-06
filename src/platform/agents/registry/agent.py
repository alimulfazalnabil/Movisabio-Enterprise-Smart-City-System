from pydantic import BaseModel
from typing import Dict, List, Optional
import enum

class RiskClass(str, enum.Enum):
    R0 = "R0" # Informational
    R1 = "R1" # Analytical
    R2 = "R2" # Decision Support
    R3 = "R3" # Operational Recommendation
    R4 = "R4" # Safety-Critical Candidate
    R5 = "R5" # Physical Control

class AutonomyMode(str, enum.Enum):
    MANUAL = "MANUAL"
    ASSISTED = "ASSISTED"
    SHADOW = "SHADOW"
    SUPERVISED_AUTOMATION = "SUPERVISED_AUTOMATION"
    LIMITED_AUTONOMY = "LIMITED_AUTONOMY"
    AUTHORIZED_AUTONOMY = "AUTHORIZED_AUTONOMY"
    FAILSAFE = "FAILSAFE"
    SUSPENDED = "SUSPENDED"

class AutonomyBudget(BaseModel):
    actions_per_hour: int
    max_risk: RiskClass
    max_duration_minutes: int

class Agent(BaseModel):
    agent_id: str
    tenant_id: str
    name: str
    domain: str
    risk_class: RiskClass
    autonomy_mode: AutonomyMode
    autonomy_budget: AutonomyBudget
    permissions: List[str]
    allowed_tools: List[str]
    
    def can_execute_action(self, action_risk: RiskClass) -> bool:
        """
        Check if the agent is allowed to execute an action based on its current autonomy mode and budget.
        """
        if self.autonomy_mode in [AutonomyMode.FAILSAFE, AutonomyMode.SUSPENDED, AutonomyMode.MANUAL]:
            return False
            
        # Simplistic risk check, real check would compare enums correctly
        risk_levels = [RiskClass.R0, RiskClass.R1, RiskClass.R2, RiskClass.R3, RiskClass.R4, RiskClass.R5]
        try:
            agent_max_idx = risk_levels.index(self.autonomy_budget.max_risk)
            action_idx = risk_levels.index(action_risk)
            if action_idx > agent_max_idx:
                return False
        except ValueError:
            return False
            
        return True
