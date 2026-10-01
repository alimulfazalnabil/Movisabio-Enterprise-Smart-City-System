import pytest
from datetime import datetime, timezone, timedelta
from src.services.priority.models.schemas import PriorityRequest, PriorityClass, PriorityStatus
from src.services.priority.engine.arbitration import PriorityArbitrationEngine

def create_mock_request(req_id: str, p_class: PriorityClass, urgency: int, eta_offset: int) -> PriorityRequest:
    return PriorityRequest(
        request_id=req_id,
        tenant_id="T1",
        vehicle_id="V1",
        vehicle_type="BUS",
        priority_class=p_class,
        route_id=None,
        current_position=None,
        heading=None,
        speed=None,
        target_intersection_id="INT-1",
        target_lane_id=None,
        estimated_arrival_time=datetime.now(timezone.utc) + timedelta(seconds=eta_offset),
        requested_phase="NS_GREEN",
        urgency=urgency,
        reason="test",
        source="GPS",
        confidence=0.9,
        status=PriorityStatus.AUTHORIZED,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
    )

def test_arbitration_selects_highest_priority_class():
    engine = PriorityArbitrationEngine()
    
    # Bus (P2) vs Ambulance (P1)
    bus_req = create_mock_request("BUS-1", PriorityClass.P2_PUBLIC_TRANSIT, urgency=5, eta_offset=30)
    amb_req = create_mock_request("AMB-1", PriorityClass.P1_EMERGENCY_SERVICE, urgency=10, eta_offset=45)
    
    winner = engine.arbitrate([bus_req, amb_req])
    
    assert winner is not None
    assert winner.request_id == "AMB-1"
    assert winner.status == PriorityStatus.GRANTED
    assert bus_req.status == PriorityStatus.PREEMPTED

def test_arbitration_breaks_ties_with_urgency():
    engine = PriorityArbitrationEngine()
    
    # Two buses, same class, different urgency
    bus1 = create_mock_request("BUS-1", PriorityClass.P2_PUBLIC_TRANSIT, urgency=5, eta_offset=30)
    bus2 = create_mock_request("BUS-2", PriorityClass.P2_PUBLIC_TRANSIT, urgency=8, eta_offset=30)
    
    winner = engine.arbitrate([bus1, bus2])
    
    assert winner.request_id == "BUS-2"

def test_arbitration_breaks_ties_with_eta():
    engine = PriorityArbitrationEngine()
    
    # Two ambulances, same class, same urgency, one arriving sooner
    amb1 = create_mock_request("AMB-1", PriorityClass.P1_EMERGENCY_SERVICE, urgency=10, eta_offset=30)
    amb2 = create_mock_request("AMB-2", PriorityClass.P1_EMERGENCY_SERVICE, urgency=10, eta_offset=15) # arriving sooner
    
    winner = engine.arbitrate([amb1, amb2])
    
    assert winner.request_id == "AMB-2"
