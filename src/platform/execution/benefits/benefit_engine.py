from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class BenefitStatus(str, enum.Enum):
    PENDING = "PENDING"
    REALIZING = "REALIZING"
    REALIZED = "REALIZED"
    LEAKING = "LEAKING"
    FAILED = "FAILED"

class Benefit(BaseModel):
    benefit_id: str
    project_id: str
    expected_value: float
    observed_value: float = 0.0
    project_status: str = "IN_PROGRESS"
    status: BenefitStatus = BenefitStatus.PENDING
    
class BenefitEngine:
    def __init__(self):
        self.benefits: Dict[str, Benefit] = {}
        
    def add_benefit(self, benefit: Benefit) -> Benefit:
        self.benefits[benefit.benefit_id] = benefit
        return benefit
        
    def detect_leakage(self, benefit_id: str) -> Benefit:
        if benefit_id not in self.benefits:
            raise ValueError("Benefit not found")
            
        benefit = self.benefits[benefit_id]
        
        if benefit.project_status == "COMPLETED":
            if benefit.observed_value < benefit.expected_value * 0.3:
                benefit.status = BenefitStatus.LEAKING
            elif benefit.observed_value >= benefit.expected_value:
                benefit.status = BenefitStatus.REALIZED
            else:
                benefit.status = BenefitStatus.REALIZING
                
        return benefit
