from src.services.nature.models.schemas import ForestChangeEvent

class ForestChangeEngine:
    def evaluate_change(self, event: ForestChangeEvent) -> str:
        """
        Evaluates a forest change event and determines if action/verification is required.
        """
        if event.verification_status == "VERIFIED":
            return "ACTION_REQUIRED" if event.change_type == "CANOPY_LOSS_CANDIDATE" else "MONITORING"
            
        if event.confidence > 0.85 and event.estimated_area_m2 > 1000:
            return "VERIFICATION_REQUIRED"
            
        return "LOGGED"
