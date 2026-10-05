import pytest
from src.services.health.models.schemas import FacilityCapacity, AmbulanceState
from src.services.health.engine.capacity import HealthCapacityEngine
from src.services.health.engine.ambulance import AmbulanceEngine

def test_health_capacity_normal():
    capacity = FacilityCapacity(
        facility_id="HOSP-01",
        total_beds=100,
        available_beds=50,
        icu_available=10,
        emergency_load_status="UNKNOWN"
    )
    engine = HealthCapacityEngine()
    status = engine.evaluate_load_status(capacity)
    assert status == "NORMAL"

def test_health_capacity_full():
    capacity = FacilityCapacity(
        facility_id="HOSP-01",
        total_beds=100,
        available_beds=2,
        icu_available=0,
        emergency_load_status="UNKNOWN"
    )
    engine = HealthCapacityEngine()
    status = engine.evaluate_load_status(capacity)
    assert status == "FULL"

def test_ambulance_dispatch():
    amb = AmbulanceState(
        ambulance_id="AMB-01",
        status="AVAILABLE",
        location="Zone-A",
        destination_facility_id=None,
        eta_minutes=None
    )
    engine = AmbulanceEngine()
    updated = engine.dispatch_ambulance(amb, "HOSP-02", 12.5)
    
    assert updated.status == "DISPATCHED"
    assert updated.destination_facility_id == "HOSP-02"
    assert updated.eta_minutes == 12.5

def test_ambulance_emergency_corridor():
    amb = AmbulanceState(
        ambulance_id="AMB-01",
        status="TRANSPORTING",
        location="Intersection-12",
        destination_facility_id="HOSP-01",
        eta_minutes=5.0
    )
    engine = AmbulanceEngine()
    corridor_needed = engine.evaluate_emergency_corridor(amb)
    
    # TRANSPORTING status should generate a corridor recommendation
    assert corridor_needed is True
