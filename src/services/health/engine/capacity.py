from src.services.health.models.schemas import FacilityCapacity

class HealthCapacityEngine:
    """
    Evaluates aggregate healthcare facility capacity.
    """
    
    def evaluate_load_status(self, capacity: FacilityCapacity) -> str:
        """
        Updates the emergency load status based on available beds and ICU capacity.
        """
        if capacity.total_beds == 0:
            return "UNKNOWN"
            
        utilization = 1.0 - (capacity.available_beds / capacity.total_beds)
        
        if utilization >= 0.95 or capacity.icu_available == 0:
            return "FULL"
        elif utilization >= 0.85 or capacity.icu_available <= 2:
            return "HIGH_LOAD"
        return "NORMAL"
