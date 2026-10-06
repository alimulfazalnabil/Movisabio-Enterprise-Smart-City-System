from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class AutonomyPolicy(BaseModel):
    policy_id: str
    allowed_actions: List[str]
    max_autonomy_hours: int
    fallback_mode: str

class EdgeAutonomyEngine:
    def __init__(self, policy: AutonomyPolicy):
        self.policy = policy
        
    def can_execute_action(self, action: str, offline_duration_hours: float) -> bool:
        """
        Determines if the edge can autonomously execute an action based on safety and policy bounds.
        """
        if offline_duration_hours > self.policy.max_autonomy_hours:
            return False # Exceeded max offline duration, must revert to fallback
            
        if action in self.policy.allowed_actions:
            return True
            
        return False
