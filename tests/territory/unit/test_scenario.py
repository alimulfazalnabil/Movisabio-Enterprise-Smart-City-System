import pytest
from src.services.territory.models.schemas import DevelopmentScenario
from src.services.territory.engine.scenario import DevelopmentScenarioEngine

def test_scenario_capacity_viable():
    engine = DevelopmentScenarioEngine()
    
    scenario = DevelopmentScenario(
        scenario_id="DEV-1",
        tenant_id="T1",
        name="New Housing",
        parcel_ids=["P-1"],
        proposed_buildings=[],
        estimated_population=100,
        estimated_water_demand_lpd=10000.0,
        estimated_energy_demand_kwh=500.0,
        estimated_trip_generation=50
    )
    
    existing_capacity = {
        "water_lpd": 50000.0,
        "energy_kwh": 2000.0,
        "traffic_trips": 1000
    }
    
    result = engine.evaluate_capacity(scenario, existing_capacity)
    
    assert result["water_impact_ratio"] == 0.2
    assert result["traffic_impact_ratio"] == 0.05
    assert result["viable"] is True

def test_scenario_capacity_breach():
    engine = DevelopmentScenarioEngine()
    
    scenario = DevelopmentScenario(
        scenario_id="DEV-2",
        tenant_id="T1",
        name="Mega Mall",
        parcel_ids=["P-1"],
        proposed_buildings=[],
        estimated_population=5000,
        estimated_water_demand_lpd=150000.0,
        estimated_energy_demand_kwh=8000.0,
        estimated_trip_generation=4500
    )
    
    existing_capacity = {
        "water_lpd": 100000.0,
        "energy_kwh": 10000.0,
        "traffic_trips": 5000
    }
    
    result = engine.evaluate_capacity(scenario, existing_capacity)
    
    assert result["water_impact_ratio"] == 1.5
    assert result["traffic_impact_ratio"] == 0.9
    assert result["viable"] is False
