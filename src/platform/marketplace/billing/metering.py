from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class UsageRecord(BaseModel):
    usage_id: str
    subscription_id: str
    metric: str
    quantity: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MeteringEngine:
    def __init__(self):
        self.usage_records: List[UsageRecord] = []
        
    def record_usage(self, record: UsageRecord):
        self.usage_records.append(record)
        
    def get_total_usage(self, subscription_id: str, metric: str) -> float:
        return sum(
            r.quantity for r in self.usage_records 
            if r.subscription_id == subscription_id and r.metric == metric
        )
