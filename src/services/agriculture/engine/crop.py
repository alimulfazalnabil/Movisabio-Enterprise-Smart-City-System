from typing import List, Dict, Any
from src.services.agriculture.models.schemas import CropState, CropHealthStatus

class CropAnomalyEngine:
    """
    Evaluates crop health based on a timeline of vegetation indices (e.g., NDVI).
    """
    
    def evaluate_timeline(self, current_state: CropState, historical_ndvi: List[float]) -> CropState:
        if not historical_ndvi or len(historical_ndvi) < 2:
            current_state.health_status = CropHealthStatus.UNKNOWN
            return current_state
            
        current_ndvi = current_state.vegetation_index
        avg_historical = sum(historical_ndvi) / len(historical_ndvi)
        
        # Sudden drop > 15% from historical average flags an anomaly candidate
        if current_ndvi < (avg_historical * 0.85):
            current_state.health_status = CropHealthStatus.ANOMALY
            current_state.confidence = 0.85
        elif current_ndvi < (avg_historical * 0.95):
            current_state.health_status = CropHealthStatus.STRESSED
            current_state.confidence = 0.70
        else:
            current_state.health_status = CropHealthStatus.HEALTHY
            current_state.confidence = 0.95
            
        return current_state
