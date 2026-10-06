from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class HealthScore(str, enum.Enum):
    HEALTHY = "HEALTHY"
    STABLE = "STABLE"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"

class CustomerHealth(BaseModel):
    tenant_id: str
    service_health_score: float = 1.0 # 0.0 to 1.0
    sla_compliance: float = 1.0
    adoption_score: float = 1.0
    outcome_achievement: float = 1.0
    support_health: float = 1.0
    last_evaluated: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def composite_health(self) -> HealthScore:
        # Simple weighted composite
        score = (
            self.service_health_score * 0.3 +
            self.sla_compliance * 0.2 +
            self.adoption_score * 0.2 +
            self.outcome_achievement * 0.2 +
            self.support_health * 0.1
        )
        if score > 0.8:
            return HealthScore.HEALTHY
        elif score > 0.6:
            return HealthScore.STABLE
        elif score > 0.4:
            return HealthScore.AT_RISK
        else:
            return HealthScore.CRITICAL

class CustomerHealthEngine:
    def __init__(self):
        self.health_records: Dict[str, CustomerHealth] = {}
        
    def evaluate_health(self, tenant_id: str, service: float, sla: float, adoption: float, outcome: float, support: float) -> CustomerHealth:
        health = CustomerHealth(
            tenant_id=tenant_id,
            service_health_score=service,
            sla_compliance=sla,
            adoption_score=adoption,
            outcome_achievement=outcome,
            support_health=support
        )
        self.health_records[tenant_id] = health
        return health
