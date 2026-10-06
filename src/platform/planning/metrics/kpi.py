from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class TerritorialKPI(BaseModel):
    kpi_id: str
    tenant_id: str
    domain: str
    metric_name: str
    target_value: float
    current_value: Optional[float] = None
    
class KPIManager:
    def evaluate_deviation(self, kpi: TerritorialKPI) -> float:
        if kpi.current_value is None:
            return 0.0
        return (kpi.current_value - kpi.target_value) / kpi.target_value
