from src.services.health.models.schemas import AmbulanceState

class AmbulanceEngine:
    """
    Coordinates ambulance routing and tracking.
    """
    
    def dispatch_ambulance(self, ambulance: AmbulanceState, facility_id: str, eta: float) -> AmbulanceState:
        """
        Updates an ambulance state for a new dispatch.
        """
        ambulance.status = "DISPATCHED"
        ambulance.destination_facility_id = facility_id
        ambulance.eta_minutes = eta
        return ambulance

    def evaluate_emergency_corridor(self, ambulance: AmbulanceState) -> bool:
        """
        Recommends an emergency signal corridor if the ambulance is actively transporting a patient.
        Returns True if a corridor recommendation is generated.
        """
        # A3.32 Rule: Provide recommendations for signal priority, but do not bypass safety layer.
        if ambulance.status in ["EN_ROUTE_TO_PATIENT", "TRANSPORTING"]:
            return True
        return False
