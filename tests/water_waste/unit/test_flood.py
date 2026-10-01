import pytest
from src.services.water_waste.models.schemas import FloodState
from src.services.water_waste.engine.flood import FloodRiskEngine

def test_flood_risk_engine_normal():
    engine = FloodRiskEngine()
    model = engine.evaluate_risk("R-1", water_level_m=0.5, rainfall_mm_h=0.0)
    assert model.state == FloodState.NORMAL

def test_flood_risk_engine_active_flood_water_level():
    engine = FloodRiskEngine()
    model = engine.evaluate_risk("R-1", water_level_m=3.5, rainfall_mm_h=5.0)
    assert model.state == FloodState.ACTIVE_FLOOD

def test_flood_risk_engine_active_flood_rainfall():
    engine = FloodRiskEngine()
    model = engine.evaluate_risk("R-1", water_level_m=1.0, rainfall_mm_h=55.0)
    assert model.state == FloodState.ACTIVE_FLOOD

def test_flood_risk_engine_high_risk():
    engine = FloodRiskEngine()
    model = engine.evaluate_risk("R-1", water_level_m=2.5, rainfall_mm_h=15.0)
    assert model.state == FloodState.HIGH_RISK
