import pytest
from datetime import datetime, timezone
from src.services.energy.models.schemas import EnergyState
from src.services.energy.engine.grid import GridConstraintEngine

def test_grid_capacity_evaluation_normal():
    engine = GridConstraintEngine()
    
    state = EnergyState(
        site_id="SITE-1",
        grid_import_kw=50.0,
        grid_export_kw=0.0,
        renewable_generation_kw=20.0,
        ev_load_kw=0.0,
        battery_charge_kw=0.0,
        battery_discharge_kw=0.0,
        building_load_kw=40.0,
        available_capacity_kw=0.0,
        timestamp=datetime.now(timezone.utc),
        quality="VALID"
    )
    
    # Net load = building_load (40) - renewable_gen (20) = 20 kW needed from grid.
    # Max connection is 100 kW. Available = 100 - 20 = 80 kW.
    available = engine.evaluate_capacity(state, 100.0)
    
    assert available == 80.0

def test_grid_capacity_with_solar_surplus():
    engine = GridConstraintEngine()
    
    state = EnergyState(
        site_id="SITE-2",
        grid_import_kw=0.0,
        grid_export_kw=30.0,
        renewable_generation_kw=80.0,
        ev_load_kw=0.0,
        battery_charge_kw=0.0,
        battery_discharge_kw=0.0,
        building_load_kw=50.0,
        available_capacity_kw=0.0,
        timestamp=datetime.now(timezone.utc),
        quality="VALID"
    )
    
    # Net load = 50 + 30 (export) - 80 (solar) = 0 kW needed from grid.
    # Actually wait: building_load + grid_export = 50 + 30 = 80
    # renewable_gen = 80
    # net load on grid = 80 - 80 = 0
    # Max connection = 100. Available = 100 - 0 = 100.
    
    available = engine.evaluate_capacity(state, 100.0)
    
    assert available == 100.0

def test_grid_capacity_prevents_negative():
    engine = GridConstraintEngine()
    
    state = EnergyState(
        site_id="SITE-3",
        grid_import_kw=110.0,
        grid_export_kw=0.0,
        renewable_generation_kw=0.0,
        ev_load_kw=0.0,
        battery_charge_kw=0.0,
        battery_discharge_kw=0.0,
        building_load_kw=110.0, # Building load exceeds grid max connection!
        available_capacity_kw=0.0,
        timestamp=datetime.now(timezone.utc),
        quality="VALID"
    )
    
    # Net load = 110 - 0 = 110
    # Max = 100
    # Available = 100 - 110 = -10 => floored to 0
    available = engine.evaluate_capacity(state, 100.0)
    
    assert available == 0.0
