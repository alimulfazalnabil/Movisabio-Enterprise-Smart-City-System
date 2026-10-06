from pydantic import BaseModel
from typing import Dict, List

class Budget(BaseModel):
    tenant_id: str
    monthly_limit: float
    warning_threshold: float
    critical_threshold: float
    currency: str = "EUR"

class BudgetEnforcer:
    def __init__(self):
        self.budgets: Dict[str, Budget] = {}
        self.current_spend: Dict[str, float] = {}
        
    def set_budget(self, budget: Budget) -> None:
        self.budgets[budget.tenant_id] = budget
        if budget.tenant_id not in self.current_spend:
            self.current_spend[budget.tenant_id] = 0.0
            
    def record_spend(self, tenant_id: str, amount: float) -> str:
        if tenant_id not in self.current_spend:
            self.current_spend[tenant_id] = 0.0
        
        self.current_spend[tenant_id] += amount
        spend = self.current_spend[tenant_id]
        
        budget = self.budgets.get(tenant_id)
        if not budget:
            return "ACTIVE"
            
        percentage = (spend / budget.monthly_limit) * 100
        
        if percentage >= 100:
            return "EXCEEDED"
        elif percentage >= budget.critical_threshold:
            return "CRITICAL"
        elif percentage >= budget.warning_threshold:
            return "WARNING"
        return "ACTIVE"
        
    def check_authorization(self, tenant_id: str, is_safety_critical: bool) -> bool:
        """Safety-critical workloads bypass budget enforcement"""
        if is_safety_critical:
            return True
            
        budget = self.budgets.get(tenant_id)
        if not budget:
            return True
            
        spend = self.current_spend.get(tenant_id, 0.0)
        return spend < budget.monthly_limit
