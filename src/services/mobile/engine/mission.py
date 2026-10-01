from src.services.mobile.models.schemas import MissionPackage

class MissionManager:
    """
    Handles lifecycle and authorization of missions for mobile assets.
    """
    
    def authorize_mission(self, mission: MissionPackage, operator_approved: bool = False) -> bool:
        """
        Validates whether a mission can transition to AUTHORIZED.
        """
        if mission.status != "PENDING_AUTHORIZATION":
            return False
            
        if mission.authorization_required and not operator_approved:
            return False
            
        mission.status = "AUTHORIZED"
        return True
        
    def abort_mission(self, mission: MissionPackage, reason: str) -> bool:
        """
        Aborts an active mission due to safety, weather, or connectivity issues.
        """
        if mission.status not in ["AUTHORIZED", "ACTIVE", "PAUSED"]:
            return False
            
        mission.status = "ABORTED"
        # Log reason for audit
        return True
