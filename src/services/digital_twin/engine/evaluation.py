import uuid
from typing import Dict, Any
from src.services.digital_twin.models.schemas import CounterfactualEvaluation

class InterventionEvaluationEngine:
    """
    Evaluates real-world interventions by comparing actual outcomes against counterfactual baseline simulations.
    """
    
    def evaluate(self, intervention_id: str, baseline_results: Dict[str, float], actual_results: Dict[str, float]) -> CounterfactualEvaluation:
        """
        baseline_results: e.g. what would have happened (from counterfactual simulation)
        actual_results: e.g. what actually happened (from live twin state)
        """
        effects = {}
        uncertainty = {}
        metrics = []
        
        for metric, baseline_val in baseline_results.items():
            if metric in actual_results:
                metrics.append(metric)
                # Effect = baseline - actual (e.g. baseline travel time 500, actual 400 => effect 100 improvement)
                effects[metric] = baseline_val - actual_results[metric]
                # Mock uncertainty calculation based on metric scale
                uncertainty[metric] = abs(effects[metric]) * 0.1 
                
        return CounterfactualEvaluation(
            evaluation_id=str(uuid.uuid4()),
            intervention_id=intervention_id,
            baseline_scenario_id="COUNTERFACTUAL_BASE",
            actual_scenario_id="ACTUAL_OBSERVED",
            metrics_compared=metrics,
            estimated_effects=effects,
            uncertainty=uncertainty
        )
