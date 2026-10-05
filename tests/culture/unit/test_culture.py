from src.services.culture.models.schemas import CulturalEvent
from src.services.culture.engine.heritage_risk import HeritageRiskEngine
from src.services.culture.engine.event_impact import EventImpactEngine

def test_heritage_risk_calculation():
    engine = HeritageRiskEngine()
    indicator = engine.calculate_risk(asset_id="MUSEUM-01", hazard=0.8, exposure=0.5, vulnerability=0.9)
    
    # 0.8 * 0.5 * 0.9 = 0.36
    assert abs(indicator.risk_score - 0.36) < 0.001
    assert indicator.asset_id == "MUSEUM-01"

def test_event_impact_simulation():
    event = CulturalEvent(
        event_id="FESTIVAL-27",
        name="Summer Music Fest",
        expected_capacity=20000,
        status="APPROVED"
    )
    
    engine = EventImpactEngine()
    impact = engine.simulate_impact(event)
    
    assert impact.transit_demand == 12000.0 # 20000 * 0.6
    assert impact.waste_demand == 10000.0 # 20000 * 0.5
    assert impact.energy_demand == 40000.0 # 20000 * 2.0
