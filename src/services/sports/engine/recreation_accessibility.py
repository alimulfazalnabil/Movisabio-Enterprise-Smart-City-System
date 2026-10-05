from src.services.sports.models.schemas import RecreationDemand, RecreationAccessibility

class RecreationAccessibilityEngine:
    def calculate_service_gap(self, demand: RecreationDemand, accessible_capacity: int) -> RecreationAccessibility:
        """
        Calculates the recreation service gap based on active population demand vs accessible capacity.
        """
        estimated_demand = int(demand.population * demand.active_population_ratio)
        gap = estimated_demand - accessible_capacity
        
        status = "LOW_GAP"
        if gap > (0.5 * estimated_demand):
            status = "CRITICAL_GAP"
        elif gap > (0.3 * estimated_demand):
            status = "HIGH_GAP"
        elif gap > (0.1 * estimated_demand):
            status = "MODERATE_GAP"
        elif gap < 0:
            gap = 0
            
        return RecreationAccessibility(
            territory_id=demand.territory_id,
            accessible_capacity=accessible_capacity,
            service_gap=gap,
            status=status
        )
