import pytest
from src.services.water_waste.models.schemas import WasteBin, WasteBinState
from src.services.water_waste.engine.waste_route import WasteRouteEngine

def test_waste_route_engine():
    engine = WasteRouteEngine()
    
    bins = [
        WasteBin(bin_id="B-1", tenant_id="T1", geometry={}, capacity_kg=100.0, waste_type="GENERAL", state=WasteBinState.EMPTY),
        WasteBin(bin_id="B-2", tenant_id="T1", geometry={}, capacity_kg=100.0, waste_type="GENERAL", state=WasteBinState.HIGH), # 80kg
        WasteBin(bin_id="B-3", tenant_id="T1", geometry={}, capacity_kg=100.0, waste_type="GENERAL", state=WasteBinState.FULL), # 100kg
        WasteBin(bin_id="B-4", tenant_id="T1", geometry={}, capacity_kg=100.0, waste_type="GENERAL", state=WasteBinState.OVERFLOW_RISK) # 110kg
    ]
    
    # Capacity is 200kg. Order of insertion should be Overflow(110) + Full(100) = 210 (too large). 
    # Wait, Overflow(110) goes in. Remaining = 90. Full(100) cannot fit. High(80) goes in. 
    # Total selected: B-4 and B-2. Total kg = 190.
    
    route = engine.generate_route("TRUCK-1", 200.0, bins)
    
    assert "B-4" in route.ordered_bin_ids
    assert "B-2" in route.ordered_bin_ids
    assert "B-3" not in route.ordered_bin_ids
    assert "B-1" not in route.ordered_bin_ids
    assert route.total_expected_kg == 190.0
