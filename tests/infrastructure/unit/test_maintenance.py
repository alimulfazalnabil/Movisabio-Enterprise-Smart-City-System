import pytest
from datetime import datetime, timezone
from src.services.infrastructure.models.schemas import AssetCondition, ConditionClass
from src.services.infrastructure.engine.maintenance import PredictiveMaintenanceEngine

def test_maintenance_engine_healthy_asset():
    engine = PredictiveMaintenanceEngine()
    condition = AssetCondition(
        asset_id="BR-1",
        timestamp=datetime.now(timezone.utc),
        condition_score=9.0,
        condition_class=ConditionClass.GOOD,
        evidence=["visual_inspection"],
        confidence=0.9,
        source="INSPECTOR"
    )
    
    risk = engine.calculate_failure_risk(condition, age_years=5.0, expected_life_years=50.0)
    
    assert risk.probability == 0.0
    assert risk.risk_level == "LOW"

def test_maintenance_engine_near_end_of_life():
    engine = PredictiveMaintenanceEngine()
    condition = AssetCondition(
        asset_id="BR-2",
        timestamp=datetime.now(timezone.utc),
        condition_score=7.0,
        condition_class=ConditionClass.FAIR,
        evidence=[],
        confidence=0.9,
        source="SYSTEM"
    )
    
    # 48 / 50 = 0.96 -> > 0.9 life ratio
    risk = engine.calculate_failure_risk(condition, age_years=48.0, expected_life_years=50.0)
    
    assert risk.probability == 0.3
    assert risk.risk_level == "LOW"

def test_maintenance_engine_poor_condition():
    engine = PredictiveMaintenanceEngine()
    condition = AssetCondition(
        asset_id="BR-3",
        timestamp=datetime.now(timezone.utc),
        condition_score=4.0,
        condition_class=ConditionClass.POOR,
        evidence=["vibration_anomaly"],
        confidence=0.9,
        source="SENSOR"
    )
    
    risk = engine.calculate_failure_risk(condition, age_years=25.0, expected_life_years=50.0)
    
    assert risk.probability == 0.4
    assert risk.risk_level == "ELEVATED"

def test_maintenance_engine_critical_and_old():
    engine = PredictiveMaintenanceEngine()
    condition = AssetCondition(
        asset_id="BR-4",
        timestamp=datetime.now(timezone.utc),
        condition_score=1.0,
        condition_class=ConditionClass.CRITICAL,
        evidence=["structural_crack"],
        confidence=0.95,
        source="INSPECTOR"
    )
    
    risk = engine.calculate_failure_risk(condition, age_years=49.0, expected_life_years=50.0)
    
    assert risk.probability == 0.99
    assert risk.risk_level == "HIGH"
