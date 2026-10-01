import pytest
from datetime import datetime, timezone, timedelta
from src.services.environment.models.schemas import EnvironmentalObservation, DataQuality
from src.services.environment.engine.quality import SensorQualityEngine

def create_base_obs(param: str, value: float, minutes_ago: int = 0) -> EnvironmentalObservation:
    return EnvironmentalObservation(
        observation_id="OBS-1",
        tenant_id="T1",
        site_id="S1",
        sensor_id="SENS-1",
        parameter=param,
        value=value,
        unit="unit",
        timestamp=datetime.now(timezone.utc) - timedelta(minutes=minutes_ago),
        confidence=0.9,
        source="IoT"
    )

def test_sensor_quality_marks_stale_data():
    engine = SensorQualityEngine()
    obs = create_base_obs("temperature", 20.0, minutes_ago=120) # 2 hours old
    
    result = engine.validate(obs)
    
    assert result.quality == DataQuality.STALE

def test_sensor_quality_marks_impossible_temp():
    engine = SensorQualityEngine()
    obs = create_base_obs("temperature", 100.0) # 100 Celsius is invalid
    
    result = engine.validate(obs)
    
    assert result.quality == DataQuality.INVALID

def test_sensor_quality_marks_negative_rainfall():
    engine = SensorQualityEngine()
    obs = create_base_obs("rainfall", -5.0)
    
    result = engine.validate(obs)
    
    assert result.quality == DataQuality.INVALID

def test_sensor_quality_accepts_valid_data():
    engine = SensorQualityEngine()
    obs = create_base_obs("PM2.5", 35.0, minutes_ago=5)
    
    result = engine.validate(obs)
    
    assert result.quality == DataQuality.VALID
