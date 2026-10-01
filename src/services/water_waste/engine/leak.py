class LeakDetectionEngine:
    """
    Evaluates water flow telemetry to identify potential leakage candidates.
    """
    
    def detect_leak_candidate(self, expected_consumption_lph: float, observed_supply_lph: float, threshold_percentage: float = 0.20) -> bool:
        """
        Returns True if the observed supply significantly exceeds expected consumption,
        indicating a candidate for leakage (or unauthorized usage/meter error).
        """
        if expected_consumption_lph <= 0:
            # Prevent division by zero; if expected is 0 but we have flow, that's definitely anomalous.
            return observed_supply_lph > 10.0 # Some absolute minimal threshold
            
        deviation = observed_supply_lph - expected_consumption_lph
        percentage = deviation / expected_consumption_lph
        
        return percentage >= threshold_percentage
