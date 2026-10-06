from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime
import enum

class ServiceHealthState(str, enum.Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"

class InfrastructureHealth(BaseModel):
    component_id: str
    tenant_id: str
    component_type: str # e.g. "EDGE_NODE", "NETWORK_LINK"
    state: ServiceHealthState = ServiceHealthState.UNKNOWN
    metrics: Dict[str, float] = Field(default_factory=dict)
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow)

class NOCEngine:
    def __init__(self):
        self.health_records: Dict[str, InfrastructureHealth] = {}
        
    def register_component(self, health: InfrastructureHealth) -> InfrastructureHealth:
        self.health_records[health.component_id] = health
        return health
        
    def report_telemetry(self, component_id: str, metrics: Dict[str, float]) -> InfrastructureHealth:
        if component_id not in self.health_records:
            raise ValueError("Component not found")
        comp = self.health_records[component_id]
        comp.metrics.update(metrics)
        comp.last_heartbeat = datetime.utcnow()
        
        # Evaluate simple threshold for demo
        if "packet_loss" in metrics and metrics["packet_loss"] > 10.0:
            comp.state = ServiceHealthState.DEGRADED
        elif "packet_loss" in metrics and metrics["packet_loss"] > 50.0:
            comp.state = ServiceHealthState.CRITICAL
        else:
            comp.state = ServiceHealthState.HEALTHY
            
        return comp
