from src.services.food.models.schemas import ColdChainObservation

class ColdChainEngine:
    def detect_deviation(self, obs: ColdChainObservation) -> str:
        """
        Analyzes a cold chain observation and determines deviation status.
        """
        status = "NORMAL"
        
        if obs.temperature_c < obs.expected_range_min or obs.temperature_c > obs.expected_range_max:
            status = "TEMPERATURE_DEVIATION"
            
            # Simulated check for severity (e.g. out of bounds by > 2 degrees)
            if obs.temperature_c > (obs.expected_range_max + 2.0) or obs.temperature_c < (obs.expected_range_min - 2.0):
                status = "SPOILAGE_RISK_CANDIDATE"
                
        if obs.door_open:
            status = "TEMPERATURE_DEVIATION" if status == "NORMAL" else status
            
        return status
