from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime
import enum

class ScenarioStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Scenario(BaseModel):
    scenario_id: str
    name: str
    tenant_id: str
    twin_id: str
    parent_scenario_id: Optional[str] = None
    baseline_snapshot_id: str
    interventions: List[Dict[str, Any]]
    simulation_engines: List[str]
    status: ScenarioStatus = ScenarioStatus.DRAFT
    
class ScenarioEngine:
    def __init__(self):
        self.scenarios: Dict[str, Scenario] = {}
        
    def create_scenario(self, scenario: Scenario) -> Scenario:
        self.scenarios[scenario.scenario_id] = scenario
        return scenario
        
    def branch_scenario(self, parent_id: str, new_name: str, new_interventions: List[Dict]) -> Scenario:
        parent = self.scenarios.get(parent_id)
        if not parent:
            raise ValueError(f"Scenario {parent_id} not found")
            
        new_scenario = Scenario(
            scenario_id=f"scen-{int(datetime.now().timestamp())}",
            name=new_name,
            tenant_id=parent.tenant_id,
            twin_id=parent.twin_id,
            parent_scenario_id=parent.scenario_id,
            baseline_snapshot_id=parent.baseline_snapshot_id,
            interventions=parent.interventions + new_interventions,
            simulation_engines=parent.simulation_engines
        )
        self.scenarios[new_scenario.scenario_id] = new_scenario
        return new_scenario
