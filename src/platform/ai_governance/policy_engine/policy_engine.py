from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class GovernancePolicy(BaseModel):
    policy_id: str
    name: str
    requires_human_approval: bool
    budget_limit: float = 0.0
    risk_class: str = "LOW"
    
class PolicyEngine:
    def __init__(self):
        self.policies: Dict[str, GovernancePolicy] = {}
        
    def add_policy(self, policy: GovernancePolicy) -> GovernancePolicy:
        self.policies[policy.policy_id] = policy
        return policy
        
    def evaluate_action(self, policy_id: str, proposed_budget: float, action_risk: str) -> Dict[str, Any]:
        if policy_id not in self.policies:
            raise ValueError("Policy not found")
            
        policy = self.policies[policy_id]
        
        result = {
            "approved": True,
            "requires_human": policy.requires_human_approval,
            "reasons": []
        }
        
        if proposed_budget > policy.budget_limit:
            result["approved"] = False
            result["reasons"].append(f"Budget exceeds policy limit of {policy.budget_limit}")
            
        if action_risk == "HIGH" and policy.risk_class == "LOW":
            result["approved"] = False
            result["reasons"].append("Action risk class exceeds policy permitted risk")
            
        return result
