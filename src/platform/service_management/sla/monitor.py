from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import enum

class SLABreachStatus(str, enum.Enum):
    MEASURED = "MEASURED"
    BREACH_CANDIDATE = "BREACH_CANDIDATE"
    VALIDATED = "VALIDATED"
    CUSTOMER_NOTIFIED = "CUSTOMER_NOTIFIED"
    REMEDIATION = "REMEDIATION"
    CLOSED = "CLOSED"

class SLABreach(BaseModel):
    breach_id: str
    customer_id: str
    metric: str
    target: float
    actual: float
    status: SLABreachStatus = SLABreachStatus.MEASURED
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SLAMonitor:
    def __init__(self):
        self.breaches: Dict[str, SLABreach] = {}
        
    def record_measurement(self, breach_id: str, customer_id: str, metric: str, target: float, actual: float) -> Optional[SLABreach]:
        # Simple threshold check, assuming lower is better (e.g. response time)
        if actual > target:
            breach = SLABreach(
                breach_id=breach_id,
                customer_id=customer_id,
                metric=metric,
                target=target,
                actual=actual,
                status=SLABreachStatus.BREACH_CANDIDATE
            )
            self.breaches[breach_id] = breach
            return breach
        return None
        
    def validate_breach(self, breach_id: str) -> SLABreach:
        if breach_id not in self.breaches:
            raise ValueError("Breach not found")
        self.breaches[breach_id].status = SLABreachStatus.VALIDATED
        return self.breaches[breach_id]
