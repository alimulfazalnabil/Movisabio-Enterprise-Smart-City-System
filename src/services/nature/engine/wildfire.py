from src.services.nature.models.schemas import WildfireObservation, WildfireRiskCandidate

class WildfireRiskEngine:
    def evaluate_risk(self, obs: WildfireObservation) -> WildfireRiskCandidate:
        """
        Evaluates wildfire risk based on environmental conditions and smoke detection.
        """
        risk_level = "LOW"
        confidence = 0.5
        
        # Basic rule-based evaluation (Temperature > 35, Humidity < 20, High Wind, Extreme Fuel)
        if obs.temperature_c > 35.0 and obs.humidity_percent < 20.0 and obs.wind_speed_kmh > 30.0:
            if obs.fuel_load in ["HIGH", "EXTREME"]:
                risk_level = "EXTREME"
                confidence = 0.8
            else:
                risk_level = "HIGH"
                confidence = 0.7
                
        # Smoke overrides environmental conditions
        if obs.smoke_detected:
            risk_level = "EXTREME"
            confidence = 0.95
            
        return WildfireRiskCandidate(
            zone_id=obs.zone_id,
            risk_level=risk_level,
            confidence=confidence
        )
