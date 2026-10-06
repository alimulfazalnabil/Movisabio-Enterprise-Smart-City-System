from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone

class Risk(BaseModel):
    risk_id: str
    tenant_id: str
    category: str
    title: str
    description: str
    asset_id: str
    likelihood: int # 1-5
    impact: int # 1-5
    inherent_risk: int = 0
    residual_risk: int = 0
    status: str = "IDENTIFIED"
    created_at: datetime
    
class RiskRegister:
    def __init__(self):
        self.risks: Dict[str, Risk] = {}
        
    def log_risk(self, risk: Risk) -> Risk:
        risk.inherent_risk = risk.likelihood * risk.impact
        risk.residual_risk = risk.inherent_risk
        self.risks[risk.risk_id] = risk
        return risk
        
    def treat_risk(self, risk_id: str, new_likelihood: int, new_impact: int, treatment_plan: str) -> bool:
        risk = self.risks.get(risk_id)
        if not risk:
            return False
            
        risk.status = "MITIGATING"
        risk.residual_risk = new_likelihood * new_impact
        return True
