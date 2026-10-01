import pytest
from datetime import datetime, timezone, timedelta
from src.services.priority.models.schemas import PriorityRequest, PriorityClass, PriorityStatus
from src.services.priority.engine.eligibility import PriorityEligibilityEngine

def create_base_request() -> PriorityRequest:
    return PriorityRequest(
        request_id="REQ-1",
        tenant_id="T1",
        vehicle_id="AMB-100",
        vehicle_type="AMBULANCE",
        priority_class=PriorityClass.P1_EMERGENCY_SERVICE,
        route_id=None,
        current_position=None,
        heading=None,
        speed=None,
        target_intersection_id="INT-1",
        target_lane_id=None,
        estimated_arrival_time=datetime.now(timezone.utc) + timedelta(minutes=1),
        requested_phase="NS_GREEN",
        urgency=10,
        reason="Medical Emergency",
        source="GPS",
        confidence=0.95,
        status=PriorityStatus.REQUESTED,
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
    )

def test_eligibility_approves_valid_request():
    engine = PriorityEligibilityEngine()
    req = create_base_request()
    registry = {
        "AMB-100": {
            "authorized": True,
            "max_priority_class": "P1"
        }
    }
    
    assert engine.evaluate(req, registry) is True
    assert req.status == PriorityStatus.AUTHORIZED

def test_eligibility_rejects_expired_request():
    engine = PriorityEligibilityEngine()
    req = create_base_request()
    req.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    
    registry = {
        "AMB-100": {
            "authorized": True,
            "max_priority_class": "P1"
        }
    }
    
    assert engine.evaluate(req, registry) is False
    assert req.status == PriorityStatus.EXPIRED

def test_eligibility_rejects_unauthorized_vehicle():
    engine = PriorityEligibilityEngine()
    req = create_base_request()
    
    registry = {
        "AMB-100": {
            "authorized": False,
            "max_priority_class": "P1"
        }
    }
    
    assert engine.evaluate(req, registry) is False
    assert req.status == PriorityStatus.REJECTED

def test_eligibility_rejects_class_escalation():
    engine = PriorityEligibilityEngine()
    req = create_base_request()
    req.priority_class = PriorityClass.P0_CRITICAL_EMERGENCY # Requesting P0
    
    registry = {
        "AMB-100": {
            "authorized": True,
            "max_priority_class": "P1" # Only authorized up to P1
        }
    }
    
    assert engine.evaluate(req, registry) is False
    assert req.status == PriorityStatus.REJECTED
