from typing import List
from src.services.earth.models.schemas import GroundwaterObservation, GroundwaterRiskState

class GroundwaterEngine:
    def evaluate_aquifer_risk(self, aquifer_id: str, observations: List[GroundwaterObservation]) -> GroundwaterRiskState:
        """
        Evaluates the risk state of an aquifer based on recent observations.
        """
        if not observations:
            return GroundwaterRiskState(aquifer_id=aquifer_id, risk_type="UNKNOWN", state="UNKNOWN", trend="UNKNOWN")
            
        # Simplified trend analysis
        avg_level = sum(obs.water_level_m for obs in observations) / len(observations)
        
        # Determine trend based on latest vs average
        latest = observations[-1].water_level_m
        if latest < avg_level * 0.9:
            trend = "DECLINING"
        elif latest > avg_level * 1.1:
            trend = "RECHARGING"
        else:
            trend = "STABLE"
            
        # Determine state
        state = "NORMAL"
        if trend == "DECLINING":
            state = "STRESSED"
            
            # Check for saltwater intrusion proxy
            if any(obs.salinity > 1.5 for obs in observations):
                state = "CRITICAL"
                
        return GroundwaterRiskState(
            aquifer_id=aquifer_id,
            risk_type="EXTRACTION_PRESSURE",
            state=state,
            trend=trend
        )
