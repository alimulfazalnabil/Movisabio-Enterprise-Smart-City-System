from typing import List, Dict
from src.services.territory.models.schemas import Parcel

class InfrastructureAccessibilityEngine:
    """
    Evaluates infrastructure gap intelligence for parcels.
    """
    
    def evaluate_gaps(self, parcel: Parcel, services_to_check: List[str]) -> Dict[str, str]:
        """
        Returns a dictionary of service -> coverage_level (e.g. HIGH, LIMITED, NONE).
        """
        gaps = {}
        for service in services_to_check:
            access = parcel.infrastructure_access.get(service, "NONE")
            if access == "NONE":
                gaps[service] = "CRITICAL_GAP"
            elif access == "LIMITED":
                gaps[service] = "WARNING"
            else:
                gaps[service] = "ADEQUATE"
                
        return gaps
