from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class ChaosScenario(str, enum.Enum):
    NODE_FAILURE = "NODE_FAILURE"
    DB_LATENCY = "DB_LATENCY"
    AI_OFFLINE = "AI_OFFLINE"
    NETWORK_PARTITION = "NETWORK_PARTITION"

class SystemState(str, enum.Enum):
    FULL = "FULL"
    DEGRADED = "DEGRADED"
    LIMITED = "LIMITED"
    OFFLINE = "OFFLINE"
    RECOVERING = "RECOVERING"

class ChaosResult(BaseModel):
    experiment_id: str
    scenario: ChaosScenario
    initial_state: SystemState
    state_during_chaos: SystemState
    final_state: SystemState
    survived: bool

class ChaosEngine:
    def __init__(self):
        self.experiments: Dict[str, ChaosResult] = {}
        
    def run_experiment(self, experiment_id: str, scenario: ChaosScenario, system_mock: Dict[str, Any]) -> ChaosResult:
        result = ChaosResult(
            experiment_id=experiment_id,
            scenario=scenario,
            initial_state=SystemState.FULL,
            state_during_chaos=SystemState.DEGRADED,
            final_state=SystemState.FULL,
            survived=True
        )
        
        if scenario == ChaosScenario.AI_OFFLINE:
            # System should degrade but survive via safety invariants
            has_safety_fallback = system_mock.get("has_safety_fallback", False)
            if not has_safety_fallback:
                result.state_during_chaos = SystemState.OFFLINE
                result.final_state = SystemState.OFFLINE
                result.survived = False
            else:
                result.state_during_chaos = SystemState.LIMITED
                
        self.experiments[experiment_id] = result
        return result
