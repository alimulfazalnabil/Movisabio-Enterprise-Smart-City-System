from src.services.sports.models.schemas import FacilityCapacity, RecreationDemand
from src.services.sports.engine.facility_capacity import FacilityCapacityEngine
from src.services.sports.engine.recreation_accessibility import RecreationAccessibilityEngine

def test_facility_capacity_utilization():
    cap = FacilityCapacity(
        facility_id="STADIUM-1",
        nominal_capacity=50000,
        scheduled_capacity=40000,
        current_occupancy=20000,
        occupancy_confidence=0.9
    )
    
    engine = FacilityCapacityEngine()
    util = engine.calculate_utilization(cap)
    
    assert util == 0.5  # 20000 / 40000
    assert not engine.check_overcapacity_risk(cap)

    # Overcapacity check
    cap.current_occupancy = 48000
    assert engine.check_overcapacity_risk(cap)

def test_recreation_accessibility_gap():
    demand = RecreationDemand(
        territory_id="ZONE-A",
        population=100000,
        active_population_ratio=0.4 # 40,000 active people
    )
    
    engine = RecreationAccessibilityEngine()
    
    # Critical gap: only 10,000 accessible capacity
    acc_crit = engine.calculate_service_gap(demand, accessible_capacity=10000)
    assert acc_crit.service_gap == 30000
    assert acc_crit.status == "CRITICAL_GAP"
    
    # Low gap: 38,000 accessible capacity
    acc_low = engine.calculate_service_gap(demand, accessible_capacity=38000)
    assert acc_low.service_gap == 2000
    assert acc_low.status == "LOW_GAP"
