import pytest
from datetime import datetime, timezone
from src.services.agriculture.models.schemas import CropState, CropHealthStatus
from src.services.agriculture.engine.crop import CropAnomalyEngine

def create_base_crop(ndvi: float) -> CropState:
    return CropState(
        field_id="F-1",
        crop_type="RICE",
        growth_stage="VEGETATIVE",
        vegetation_index=ndvi,
        moisture_indicator=0.5,
        temperature_stress=0.2,
        confidence=0.0,
        observation_time=datetime.now(timezone.utc)
    )

def test_crop_engine_detects_anomaly_on_sudden_drop():
    engine = CropAnomalyEngine()
    
    # Historical NDVI: 0.6, 0.65, 0.62 (avg ~ 0.623)
    # 15% drop is < 0.53
    current = create_base_crop(0.48)
    
    result = engine.evaluate_timeline(current, [0.6, 0.65, 0.62])
    
    assert result.health_status == CropHealthStatus.ANOMALY
    assert result.confidence == 0.85

def test_crop_engine_detects_stress_on_minor_drop():
    engine = CropAnomalyEngine()
    
    # Avg ~ 0.623
    # 5% drop is < 0.59
    current = create_base_crop(0.55)
    
    result = engine.evaluate_timeline(current, [0.6, 0.65, 0.62])
    
    assert result.health_status == CropHealthStatus.STRESSED
    assert result.confidence == 0.70

def test_crop_engine_detects_healthy_baseline():
    engine = CropAnomalyEngine()
    
    current = create_base_crop(0.63)
    
    result = engine.evaluate_timeline(current, [0.6, 0.65, 0.62])
    
    assert result.health_status == CropHealthStatus.HEALTHY
    assert result.confidence == 0.95
