from typing import Dict, Any

class ModelValidator:
    def validate_simulation(self, observed_metrics: Dict[str, float], simulated_metrics: Dict[str, float]) -> Dict[str, float]:
        """
        Calculates error between simulated results and observed reality.
        """
        errors = {}
        for metric, observed_val in observed_metrics.items():
            simulated_val = simulated_metrics.get(metric)
            if simulated_val is not None and observed_val != 0:
                # MAPE (Mean Absolute Percentage Error) for single point
                error = abs((observed_val - simulated_val) / observed_val)
                errors[metric] = error
                
        return errors
