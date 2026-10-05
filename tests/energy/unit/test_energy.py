from src.services.energy.models.schemas import CriticalLoadAsset
from src.services.energy.engine.grid_congestion import GridCongestionEngine
from src.services.energy.engine.outage_impact import OutageImpactEngine

def test_grid_congestion():
    engine = GridCongestionEngine()
    
    # Normal load
    state_normal = engine.evaluate_congestion("TX-1", "ZONE-A", load_kw=400, capacity_kw=1000)
    assert state_normal.state == "NORMAL"
    
    # Congested load
    state_congested = engine.evaluate_congestion("TX-1", "ZONE-A", load_kw=960, capacity_kw=1000)
    assert state_congested.state == "CONGESTED"
    
    # Failure risk load
    state_risk = engine.evaluate_congestion("TX-1", "ZONE-A", load_kw=1100, capacity_kw=1000)
    assert state_risk.state == "FAILURE_RISK"

def test_outage_impact():
    engine = OutageImpactEngine()
    
    hospital = CriticalLoadAsset(
        asset_id="HOSPITAL-1",
        asset_type="HOSPITAL",
        criticality="CRITICAL",
        backup_capacity_kw=500,
        backup_duration_minutes=1440
    )
    
    pump = CriticalLoadAsset(
        asset_id="WATER-PUMP-1",
        asset_type="WATER_PUMP",
        criticality="HIGH",
        backup_capacity_kw=100,
        backup_duration_minutes=240
    )
    
    feeder_map = {
        "FEEDER-A": [hospital],
        "FEEDER-B": [pump]
    }
    
    outage = engine.assess_impact("OUTAGE-001", ["FEEDER-A"], feeder_map)
    
    assert outage.status == "IMPACT_ASSESSED"
    assert "HOSPITAL-1" in outage.affected_critical_loads
    assert "WATER-PUMP-1" not in outage.affected_critical_loads
