from datetime import datetime, timezone
from src.services.environment.models.schemas import EnvironmentalObservation, DataQuality

class SensorQualityEngine:
    """
    Validates raw environmental observations and flags stale, impossible, or suspect data.
    """
    
    def validate(self, observation: EnvironmentalObservation) -> EnvironmentalObservation:
        # 1. Freshness check
        age_seconds = (datetime.now(timezone.utc) - observation.timestamp).total_seconds()
        if age_seconds > 3600: # Older than 1 hour
            observation.quality = DataQuality.STALE
            return observation
            
        # 2. Impossible values (example constraints)
        val = observation.value
        param = observation.parameter
        
        if param == "temperature":
            if val < -60 or val > 60:
                observation.quality = DataQuality.INVALID
                return observation
        elif param in ["PM2.5", "PM10", "rainfall", "humidity"]:
            if val < 0:
                observation.quality = DataQuality.INVALID
                return observation
        
        # If all checks pass
        observation.quality = DataQuality.VALID
        return observation
