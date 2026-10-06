from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid

class UsageRecord(BaseModel):
    usage_id: str
    tenant_id: str
    service: str
    operation: str
    resource_type: str
    quantity: float
    unit: str
    usage_time: datetime
    
class UsageLedger:
    def __init__(self):
        self.records: List[UsageRecord] = []
        
    def record_usage(self, tenant_id: str, service: str, operation: str, resource_type: str, quantity: float, unit: str) -> UsageRecord:
        record = UsageRecord(
            usage_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            service=service,
            operation=operation,
            resource_type=resource_type,
            quantity=quantity,
            unit=unit,
            usage_time=datetime.now(timezone.utc)
        )
        self.records.append(record)
        return record
        
    def get_total_usage(self, tenant_id: str, resource_type: str) -> float:
        return sum(r.quantity for r in self.records if r.tenant_id == tenant_id and r.resource_type == resource_type)
