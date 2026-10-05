from src.services.sports.models.schemas import FacilityCapacity

class FacilityCapacityEngine:
    def calculate_utilization(self, capacity_data: FacilityCapacity) -> float:
        """
        Calculates the current utilization ratio of a facility based on scheduled capacity.
        Returns a float between 0 and 1.
        """
        if capacity_data.scheduled_capacity <= 0:
            return 0.0
        
        utilization = capacity_data.current_occupancy / capacity_data.scheduled_capacity
        return min(utilization, 1.0)
    
    def check_overcapacity_risk(self, capacity_data: FacilityCapacity) -> bool:
        """
        Checks if current occupancy exceeds 95% of nominal capacity.
        """
        if capacity_data.nominal_capacity <= 0:
            return False
            
        return (capacity_data.current_occupancy / capacity_data.nominal_capacity) > 0.95
