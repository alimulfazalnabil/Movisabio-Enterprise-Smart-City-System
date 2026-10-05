from src.services.food.models.schemas import ColdChainObservation
from src.services.food.engine.cold_chain import ColdChainEngine
from src.services.food.engine.food_security import FoodSecurityEngine

def test_cold_chain_deviation():
    obs_normal = ColdChainObservation(
        observation_id="OBS-1",
        unit_id="TRUCK-A",
        temperature_c=2.0,
        expected_range_min=0.0,
        expected_range_max=4.0,
        humidity_percent=85.0,
        door_open=False
    )
    
    engine = ColdChainEngine()
    
    assert engine.detect_deviation(obs_normal) == "NORMAL"
    
    # Deviation check
    obs_normal.temperature_c = 5.0
    assert engine.detect_deviation(obs_normal) == "TEMPERATURE_DEVIATION"
    
    # Spoilage risk check
    obs_normal.temperature_c = 8.0
    assert engine.detect_deviation(obs_normal) == "SPOILAGE_RISK_CANDIDATE"

def test_food_security_risk():
    engine = FoodSecurityEngine()
    
    risk_critical = engine.calculate_territory_risk(0.3, 0.4, 0.3, 0.2, "ZONE-1")
    assert risk_critical.risk_level == "CRITICAL"
    
    risk_low = engine.calculate_territory_risk(0.9, 0.8, 0.9, 0.9, "ZONE-2")
    assert risk_low.risk_level == "LOW"
