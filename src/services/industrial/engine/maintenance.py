from src.services.industrial.models.schemas import MachineAsset, MaintenancePrediction

class PredictiveMaintenanceEngine:
    """
    Predicts remaining useful life (RUL) and recommends maintenance.
    """
    
    def predict_maintenance(self, asset: MachineAsset) -> MaintenancePrediction:
        """
        Calculates a rough RUL based on operating hours vs maintenance interval.
        """
        hours_remaining = asset.maintenance_interval_hours - asset.operating_hours
        
        # Convert to days (assume 24h operation)
        days_remaining = hours_remaining / 24.0
        
        # Provide an interval, e.g., +/- 10%
        margin = max(1, int(days_remaining * 0.1))
        
        rul_min = int(days_remaining - margin)
        rul_max = int(days_remaining + margin)
        
        action = "SCHEDULE_MAINTENANCE" if rul_min <= 7 else "MONITOR"
        
        return MaintenancePrediction(
            asset_id=asset.asset_id,
            rul_min_days=max(0, rul_min),
            rul_max_days=max(0, rul_max),
            confidence=0.85,
            recommended_action=action
        )
