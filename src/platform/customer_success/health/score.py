from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime
import enum

class HealthState(str, enum.Enum):
    HEALTHY = "HEALTHY"
    WATCH = "WATCH"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"
    RECOVERY = "RECOVERY"

class CustomerHealth(BaseModel):
    customer_id: str
    overall_score: int
    state: HealthState
    factors: Dict[str, int] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class HealthEngine:
    def __init__(self):
        self.health_records: Dict[str, CustomerHealth] = {}
        
    def calculate_health(self, customer_id: str, factors: Dict[str, int]) -> CustomerHealth:
        # Simple average of factors for now
        overall = sum(factors.values()) // len(factors) if factors else 0
        
        state = HealthState.HEALTHY
        if overall < 40:
            state = HealthState.CRITICAL
        elif overall < 60:
            state = HealthState.AT_RISK
        elif overall < 80:
            state = HealthState.WATCH
            
        record = CustomerHealth(
            customer_id=customer_id,
            overall_score=overall,
            state=state,
            factors=factors
        )
        self.health_records[customer_id] = record
        return record
