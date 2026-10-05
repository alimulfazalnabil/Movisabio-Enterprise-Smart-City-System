from src.services.logistics.models.schemas import LoadingZone

class CurbManagementEngine:
    """
    Manages loading zone availability and detects violations.
    """
    
    def process_arrival(self, zone: LoadingZone) -> str:
        """
        Processes a vehicle arrival at a loading zone.
        """
        if zone.status == "OUT_OF_SERVICE":
            return "REJECTED_OUT_OF_SERVICE"
            
        if zone.current_occupancy >= zone.capacity:
            return "REJECTED_FULL"
            
        zone.current_occupancy += 1
        if zone.current_occupancy >= zone.capacity:
            zone.status = "OCCUPIED"
            
        return "ACCEPTED"
        
    def process_departure(self, zone: LoadingZone) -> None:
        """
        Processes a vehicle departure from a loading zone.
        """
        if zone.current_occupancy > 0:
            zone.current_occupancy -= 1
            if zone.status == "OCCUPIED":
                zone.status = "AVAILABLE"
