from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime, timedelta
import enum

class RenewalRisk(str, enum.Enum):
    LOW_RISK = "LOW_RISK"
    WATCH = "WATCH"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"

class RenewalOpportunity(BaseModel):
    renewal_id: str
    customer_id: str
    subscription_id: str
    expiry_date: datetime
    risk: RenewalRisk = RenewalRisk.WATCH
    factors: List[str] = Field(default_factory=list)

class RenewalEngine:
    def __init__(self):
        self.opportunities: Dict[str, RenewalOpportunity] = {}
        
    def analyze_renewal(self, renewal: RenewalOpportunity, health_score: int, open_p1_tickets: int) -> RenewalOpportunity:
        risk = RenewalRisk.LOW_RISK
        factors = []
        
        if health_score < 60:
            risk = RenewalRisk.AT_RISK
            factors.append("Low Health Score")
            
        if open_p1_tickets > 0:
            risk = RenewalRisk.CRITICAL
            factors.append("Open Critical Support Tickets")
            
        renewal.risk = risk
        renewal.factors = factors
        self.opportunities[renewal.renewal_id] = renewal
        return renewal
