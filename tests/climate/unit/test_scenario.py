import pytest
from datetime import datetime, timezone
from src.services.climate.models.schemas import ClimateScenario
from src.services.climate.engine.scenario import ScenarioSimulationEngine

def test_scenario_ev_adoption():
    engine = ScenarioSimulationEngine()
    
    scenario = ClimateScenario(
        scenario_id="SCEN-1",
        tenant_id="T1",
        name="30% EV Adoption",
        baseline_id="BASE-1",
        assumptions={},
        interventions=[
            {"type": "EV_ADOPTION", "target_percentage": 30.0}
        ],
        time_horizon_years=5,
        created_at=datetime.now(timezone.utc),
        status="DRAFT"
    )
    
    baseline_emissions = 10000.0 # 10,000 kg
    
    result = engine.simulate_ev_adoption_impact(scenario, baseline_emissions)
    
    assert result["scenario_emissions_kg"] == 7000.0
    assert result["avoided_emissions_kg"] == 3000.0

def test_scenario_invalid_target():
    engine = ScenarioSimulationEngine()
    
    scenario = ClimateScenario(
        scenario_id="SCEN-2",
        tenant_id="T1",
        name="Invalid EV Adoption",
        baseline_id="BASE-1",
        assumptions={},
        interventions=[
            {"type": "EV_ADOPTION", "target_percentage": 150.0}
        ],
        time_horizon_years=5,
        created_at=datetime.now(timezone.utc),
        status="DRAFT"
    )
    
    with pytest.raises(ValueError):
        engine.simulate_ev_adoption_impact(scenario, 10000.0)
