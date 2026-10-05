import pytest
from src.services.buildings.models.schemas import BuildingEnergy
from src.services.buildings.engine.energy import EnergyManagementEngine

def test_demand_response():
    engine = EnergyManagementEngine()
    
    energy = BuildingEnergy(
        building_id="B1", current_kw=100.0, baseline_kw=100.0, dr_active=False
    )
    
    # Grid becomes critical
    res1 = engine.evaluate_demand_response(energy, grid_critical=True)
    assert res1.dr_active == True
    assert res1.current_kw == 80.0
    
    # Grid normalizes
    res2 = engine.evaluate_demand_response(energy, grid_critical=False)
    assert res2.dr_active == False
    assert res2.current_kw == 100.0
