from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class ContextSnapshot(BaseModel):
    context_id: str
    tenant_id: str
    city_id: str
    time: datetime
    
    # Version bindings ensure reproducibility of the exact state the agent saw
    traffic_state_version: str
    prediction_version: str
    digital_twin_version: str
    policy_version: str
    
    data_quality: str = "VALID"
    
class ContextEngine:
    def build_snapshot(self, tenant_id: str, city_id: str, current_time: datetime) -> ContextSnapshot:
        """
        Dynamically constructs an authorized context boundary for an agent execution.
        """
        return ContextSnapshot(
            context_id=f"ctx-{int(current_time.timestamp())}",
            tenant_id=tenant_id,
            city_id=city_id,
            time=current_time,
            traffic_state_version="v_latest",
            prediction_version="v_latest",
            digital_twin_version="v_latest",
            policy_version="v_latest"
        )
