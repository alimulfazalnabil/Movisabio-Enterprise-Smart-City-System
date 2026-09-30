import pytest
from aitcs.application.public_transport_engine import TransitSignalPriorityEngine, TransitPriorityRequest
from aitcs.application.smart_parking_engine import SmartParkingEngine

def test_transit_signal_priority():
    engine = TransitSignalPriorityEngine()
    req = TransitPriorityRequest(
        vehicle_id="BRT-09",
        transit_type="BRT",
        intersection_id="INT-001",
        route_number="Line-5",
        estimated_arrival_seconds=12,
        passenger_count=45
    )
    decision = engine.evaluate_transit_priority(req)
    assert decision.action_taken == "GREEN_EXTENDED"
    assert decision.extension_seconds == 15

def test_smart_parking_engine():
    engine = SmartParkingEngine()
    status = engine.get_zone_status("PARK-CENTRAL-01")
    assert status.total_slots == 150
    assert status.available_slots == 30
    assert status.occupancy_percentage == 80.0
