from datetime import datetime, timezone
from typing import List
from src.services.water_waste.models.schemas import FloodRiskModel, FloodState

class FloodRiskEngine:
    """
    Evaluates rainfall and water level telemetry to produce a territorial flood risk model.
    """
    
    def evaluate_risk(self, region_id: str, water_level_m: float, rainfall_mm_h: float) -> FloodRiskModel:
        """
        Calculates flood risk based on simulated thresholds.
        """
        state = FloodState.NORMAL
        confidence = 0.9
        
        if water_level_m > 3.0 or rainfall_mm_h > 50.0:
            state = FloodState.ACTIVE_FLOOD
            confidence = 0.95
        elif water_level_m > 2.0 or rainfall_mm_h > 20.0:
            state = FloodState.HIGH_RISK
        elif water_level_m > 1.5 or rainfall_mm_h > 10.0:
            state = FloodState.ELEVATED
        elif rainfall_mm_h > 0:
            state = FloodState.WATCH
            
        return FloodRiskModel(
            region_id=region_id,
            timestamp=datetime.now(timezone.utc),
            state=state,
            water_level_m=water_level_m,
            rainfall_mm_h=rainfall_mm_h,
            confidence=confidence,
            affected_assets=[]
        )
