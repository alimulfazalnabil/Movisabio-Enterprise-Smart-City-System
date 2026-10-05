import pytest
from src.services.industrial.models.schemas import MachineAsset
from src.services.industrial.engine.maintenance import PredictiveMaintenanceEngine

def test_predictive_maintenance():
    engine = PredictiveMaintenanceEngine()
    
    asset_urgent = MachineAsset(
        asset_id="M1", asset_type="CNC", status="RUNNING",
        operating_hours=9800, maintenance_interval_hours=10000
    )
    
    pred_urgent = engine.predict_maintenance(asset_urgent)
    # 200 hours left / 24 = 8.33 days, margin = 1 -> rul_min = 7.
    assert pred_urgent.recommended_action == "SCHEDULE_MAINTENANCE"
    
    asset_critical = MachineAsset(
        asset_id="M2", asset_type="CNC", status="RUNNING",
        operating_hours=9900, maintenance_interval_hours=10000
    )
    
    pred_critical = engine.predict_maintenance(asset_critical)
    # 100 hours left / 24 = 4.16 days -> action SCHEDULE_MAINTENANCE
    assert pred_critical.recommended_action == "SCHEDULE_MAINTENANCE"
