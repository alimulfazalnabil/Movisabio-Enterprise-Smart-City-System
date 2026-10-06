from pydantic import BaseModel
from typing import Dict, Any

class SLO(BaseModel):
    service_id: str
    indicator: str
    target: float
    window: str

class ErrorBudget:
    def __init__(self, slo: SLO):
        self.slo = slo
        self.total_requests = 0
        self.failed_requests = 0
        
    def record_request(self, success: bool):
        self.total_requests += 1
        if not success:
            self.failed_requests += 1
            
    def is_budget_exhausted(self) -> bool:
        if self.total_requests == 0:
            return False
            
        success_rate = (self.total_requests - self.failed_requests) / self.total_requests
        return success_rate < self.slo.target
