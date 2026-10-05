from src.services.education.models.schemas import CampusOccupancy

class CampusEngine:
    def evaluate_occupancy(self, occupancy: CampusOccupancy) -> str:
        """
        Evaluates campus occupancy and returns a status.
        """
        if occupancy.peak_capacity == 0:
            return "UNKNOWN"
            
        utilization = occupancy.current_occupancy / occupancy.peak_capacity
        
        if utilization > 0.95:
            return "OVERCAPACITY_CANDIDATE"
        elif utilization < 0.30:
            return "UNDERUTILIZED"
        return "OPTIMAL"
