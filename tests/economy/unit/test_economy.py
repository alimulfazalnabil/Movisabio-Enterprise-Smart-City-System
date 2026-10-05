from datetime import datetime
from src.services.economy.models.schemas import EconomicActivityIndicator, EconomicShockEvent, EconomicResilience
from src.services.economy.engine.activity import EconomicActivityEngine
from src.services.economy.engine.shock import EconomicShockEngine

def test_composite_index():
    indicator = EconomicActivityIndicator(
        zone_id="ZONE-COMM-01",
        business_activity_score=80.0,
        retail_activity_score=90.0,
        mobility_score=70.0,
        tourism_score=50.0,
        calculation_timestamp=datetime.utcnow()
    )
    engine = EconomicActivityEngine()
    result = engine.calculate_composite_index(indicator)
    # 80*0.4 + 90*0.3 + 70*0.15 + 50*0.15 = 32.0 + 27.0 + 10.5 + 7.5 = 77.0
    assert result.composite_index == 77.0

def test_shock_impact_severe():
    event = EconomicShockEvent(
        event_id="SHOCK-01",
        shock_type="SUPPLY_CHAIN_FAILURE",
        affected_zones=["ZONE-COMM-01"],
        severity="HIGH" # base 3.0
    )
    resilience = EconomicResilience(
        zone_id="ZONE-COMM-01",
        diversity_score=0.4,
        infrastructure_score=0.6,
        resilience_index=0.5 # adjusted: 3.0 / 0.5 = 6.0
    )
    engine = EconomicShockEngine()
    impact = engine.evaluate_impact(event, resilience)
    assert impact == "SEVERE_DISRUPTION"

def test_shock_impact_manageable():
    event = EconomicShockEvent(
        event_id="SHOCK-02",
        shock_type="TOURISM_SHOCK",
        affected_zones=["ZONE-COMM-02"],
        severity="MODERATE" # base 2.0
    )
    resilience = EconomicResilience(
        zone_id="ZONE-COMM-02",
        diversity_score=0.9,
        infrastructure_score=0.9,
        resilience_index=1.2 # adjusted: 2.0 / 1.2 = 1.66
    )
    engine = EconomicShockEngine()
    impact = engine.evaluate_impact(event, resilience)
    assert impact == "MANAGEABLE"
