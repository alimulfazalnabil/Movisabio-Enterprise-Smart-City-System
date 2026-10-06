from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class ScenarioType(str, enum.Enum):
    BASELINE = "BASELINE"
    GROWTH = "GROWTH"
    CONSERVATIVE = "CONSERVATIVE"
    STRESS = "STRESS"
    TRANSFORMATION = "TRANSFORMATION"

class Scenario(BaseModel):
    scenario_id: str
    name: str
    scenario_type: ScenarioType
    assumptions: Dict[str, float] = Field(default_factory=dict)
    projected_revenue: float = 0.0
    projected_cost: float = 0.0
    projected_risk_score: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ScenarioEngine:
    def __init__(self):
        self.scenarios: Dict[str, Scenario] = {}
        
    def create_scenario(self, scenario: Scenario) -> Scenario:
        self.scenarios[scenario.scenario_id] = scenario
        return scenario
        
    def simulate(self, scenario_id: str, base_revenue: float, base_cost: float) -> Scenario:
        if scenario_id not in self.scenarios:
            raise ValueError("Scenario not found")
            
        scenario = self.scenarios[scenario_id]
        
        # Simple strategic what-if model
        growth_multiplier = scenario.assumptions.get("customer_growth_rate", 1.0)
        cost_multiplier = scenario.assumptions.get("cloud_cost_increase", 1.0)
        
        scenario.projected_revenue = base_revenue * growth_multiplier
        scenario.projected_cost = base_cost * cost_multiplier
        
        # Simple risk model
        if scenario.projected_cost > scenario.projected_revenue:
            scenario.projected_risk_score = 0.9 # High financial risk
        else:
            scenario.projected_risk_score = 0.2
            
        return scenario
