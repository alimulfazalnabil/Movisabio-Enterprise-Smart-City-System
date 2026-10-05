from typing import List
from src.services.logistics.models.schemas import LogisticsFacility

class FacilityIntelligenceEngine:
    """
    Monitors logistics facilities and detects congestion or capacity constraints.
    """
    
    def evaluate_facility_status(self, facility: LogisticsFacility) -> str:
        """
        Updates the facility status based on current load and truck queues.
        """
        utilization = facility.current_load / facility.capacity if facility.capacity > 0 else 0
        
        if utilization >= 0.95 or facility.truck_queue_length > 20:
            return "CONGESTED"
        elif utilization >= 0.85 or facility.truck_queue_length > 10:
            return "HIGH_LOAD"
        return "NORMAL"
