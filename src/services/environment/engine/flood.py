from typing import List
from src.services.environment.models.schemas import EnvironmentalObservation, EnvironmentalRisk, RiskType

class FloodRiskEngine:
    """
    Evaluates flood risk based on rainfall, water levels, and other environmental observations.
    """
    
    def evaluate_risk(self, observations: List[EnvironmentalObservation], territory_id: str) -> EnvironmentalRisk:
        # Simple heuristic combining rainfall and water levels
        rainfall_obs = [o for o in observations if o.parameter == "rainfall" and o.quality == "VALID"]
        water_level_obs = [o for o in observations if o.parameter == "water_level" and o.quality == "VALID"]
        
        avg_rainfall = sum(o.value for o in rainfall_obs) / max(len(rainfall_obs), 1)
        avg_water_level = sum(o.value for o in water_level_obs) / max(len(water_level_obs), 1)
        
        severity = "LOW"
        prob = 0.1
        
        if avg_rainfall > 50 or avg_water_level > 2.0:
            severity = "CRITICAL"
            prob = 0.95
        elif avg_rainfall > 20 or avg_water_level > 1.0:
            severity = "HIGH"
            prob = 0.7
            
        return EnvironmentalRisk(
            risk_id="RISK-FLOOD-" + territory_id,
            tenant_id="T1",
            territory_id=territory_id,
            risk_type=RiskType.FLOOD,
            severity=severity,
            probability=prob,
            spatial_extent=None,
            evidence=[f"Rainfall={avg_rainfall}mm", f"WaterLevel={avg_water_level}m"],
            confidence=0.85,
            model_version="v1.0",
            status="ACTIVE"
        )
