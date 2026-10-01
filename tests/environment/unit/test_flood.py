import pytest
from datetime import datetime, timezone
from src.services.environment.models.schemas import EnvironmentalObservation, DataQuality, RiskType
from src.services.environment.engine.flood import FloodRiskEngine

def create_obs(param: str, value: float) -> EnvironmentalObservation:
    return EnvironmentalObservation(
        observation_id="OBS-1",
        tenant_id="T1",
        site_id="S1",
        sensor_id="SENS-1",
        parameter=param,
        value=value,
        unit="unit",
        timestamp=datetime.now(timezone.utc),
        quality=DataQuality.VALID,
        confidence=0.9,
        source="IoT"
    )

def test_flood_engine_detects_low_risk():
    engine = FloodRiskEngine()
    obs = [
        create_obs("rainfall", 2.0),
        create_obs("water_level", 0.1)
    ]
    
    risk = engine.evaluate_risk(obs, "TERR-1")
    
    assert risk.risk_type == RiskType.FLOOD
    assert risk.severity == "LOW"

def test_flood_engine_detects_critical_risk_on_heavy_rain():
    engine = FloodRiskEngine()
    obs = [
        create_obs("rainfall", 65.0), # > 50
        create_obs("water_level", 0.5)
    ]
    
    risk = engine.evaluate_risk(obs, "TERR-2")
    
    assert risk.severity == "CRITICAL"
    assert risk.probability == 0.95
