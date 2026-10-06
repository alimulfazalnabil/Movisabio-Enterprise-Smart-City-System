from pydantic import BaseModel
from typing import Dict, Any, List
import enum

class PolicyStatus(str, enum.Enum):
    PROPOSED = "PROPOSED"
    SIMULATED = "SIMULATED"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    ACTIVATED = "ACTIVATED"

class Policy(BaseModel):
    policy_id: str
    name: str
    domain: str
    status: PolicyStatus = PolicyStatus.PROPOSED
    rules: List[Dict[str, Any]]
    
class PolicyGovernanceEngine:
    def __init__(self):
        self.policies: Dict[str, Policy] = {}
        
    def submit_policy_proposal(self, policy: Policy):
        self.policies[policy.policy_id] = policy
        
    def approve_policy(self, policy_id: str, approver_id: str):
        if policy_id in self.policies:
            self.policies[policy_id].status = PolicyStatus.APPROVED
