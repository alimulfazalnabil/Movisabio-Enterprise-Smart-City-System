from pydantic import BaseModel
from typing import List, Dict, Any

class ScenarioResult(BaseModel):
    scenario_id: str
    option_id: str
    metrics: Dict[str, float]
    robustness_score: float

class SimulationEngine:
    def simulate_options(self, context: Dict[str, Any], options: List[Dict[str, Any]]) -> List[ScenarioResult]:
        """
        Simulates candidate options against multiple environmental scenarios.
        """
        results = []
        for opt in options:
            # Simulated Digital Twin evaluation
            base_score = opt.get("base_score", 0.0)
            
            # Evaluate under different hypothetical scenarios
            normal_perf = base_score * 1.0
            rain_perf = base_score * 0.8
            incident_perf = base_score * 0.4
            
            robustness = (normal_perf + rain_perf + incident_perf) / 3.0
            
            results.append(ScenarioResult(
                scenario_id="sim-run-1",
                option_id=opt["option_id"],
                metrics={"normal": normal_perf, "rain": rain_perf, "incident": incident_perf},
                robustness_score=robustness
            ))
            
        return results
