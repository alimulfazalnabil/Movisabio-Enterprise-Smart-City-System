from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class StressScenarioType(str, enum.Enum):
    FINANCIAL = "FINANCIAL"
    WORKFORCE = "WORKFORCE"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    MARKET = "MARKET"
    SECURITY = "SECURITY"

class StressScenario(BaseModel):
    scenario_id: str
    name: str
    type: StressScenarioType
    parameters: Dict[str, float] = Field(default_factory=dict)
    
class ResilienceAssessment(BaseModel):
    scenario_id: str
    survivability_score: float # 0.0 to 1.0
    critical_failures: List[str] = Field(default_factory=list)
    recommended_mitigations: List[str] = Field(default_factory=list)

class StressTester:
    def __init__(self):
        self.scenarios: Dict[str, StressScenario] = {}
        
    def define_scenario(self, scenario: StressScenario) -> StressScenario:
        self.scenarios[scenario.scenario_id] = scenario
        return scenario
        
    def run_stress_test(self, scenario_id: str, current_cash_reserves: float, current_capacity: int) -> ResilienceAssessment:
        if scenario_id not in self.scenarios:
            raise ValueError("Scenario not found")
            
        scenario = self.scenarios[scenario_id]
        
        assessment = ResilienceAssessment(scenario_id=scenario_id, survivability_score=1.0)
        
        if scenario.type == StressScenarioType.FINANCIAL:
            rev_drop = scenario.parameters.get("revenue_drop_pct", 0.0)
            cost_spike = scenario.parameters.get("cost_spike_pct", 0.0)
            
            # Simple mock logic
            if rev_drop > 0.2 and current_cash_reserves < 5000000:
                assessment.survivability_score = 0.4
                assessment.critical_failures.append("Cash flow exhaustion within 6 months")
                assessment.recommended_mitigations.append("Secure backup credit line")
                
        elif scenario.type == StressScenarioType.WORKFORCE:
            capacity_drop = scenario.parameters.get("capacity_drop_pct", 0.0)
            if capacity_drop > 0.15:
                assessment.survivability_score = 0.6
                assessment.critical_failures.append("Unable to meet SLA for Tier 1 customers")
                assessment.recommended_mitigations.append("Cross-train tier 2 support teams")
                
        return assessment
