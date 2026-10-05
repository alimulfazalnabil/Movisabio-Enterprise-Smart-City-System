from typing import List
from src.services.earth.models.schemas import GeologicalHazardObservation, HazardRiskCandidate

class GeologicalHazardEngine:
    def detect_hazard_risk(self, obs: GeologicalHazardObservation, exposed_assets: List[str]) -> HazardRiskCandidate:
        """
        Translates a geological hazard observation into a territorial risk candidate.
        """
        risk_level = "LOW"
        
        if obs.severity == "HIGH":
            risk_level = "CRITICAL" if len(exposed_assets) > 0 else "HIGH"
        elif obs.severity == "MODERATE":
            risk_level = "MODERATE"
            
        return HazardRiskCandidate(
            zone_id=obs.zone_id,
            hazard_type=obs.hazard_type,
            risk_level=risk_level,
            exposed_infrastructure=exposed_assets
        )
