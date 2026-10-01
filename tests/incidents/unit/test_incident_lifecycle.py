import pytest
from datetime import datetime, timezone
from src.services.incidents.models.schemas import Incident, IncidentType, IncidentStatus, IncidentSeverity
from src.services.incidents.lifecycle.state_machine import IncidentStateMachine

def test_valid_status_transition():
    incident = Incident(
        incident_id="INC-001",
        tenant_id="T1",
        city_id="C1",
        site_id="S1",
        incident_type=IncidentType.LANE_BLOCKAGE,
        status=IncidentStatus.DETECTED,
        severity=IncidentSeverity.MEDIUM,
        confidence=0.9,
        detected_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        source_ids=[],
        evidence=[],
        affected_lanes=[],
        affected_signal_groups=[],
        description="Test"
    )
    
    # Valid transition DETECTED -> CANDIDATE
    success = IncidentStateMachine.transition(incident, IncidentStatus.CANDIDATE, "system")
    assert success is True
    assert incident.status == IncidentStatus.CANDIDATE
    
    # Valid transition CANDIDATE -> CONFIRMED
    success = IncidentStateMachine.transition(incident, IncidentStatus.CONFIRMED, "operator")
    assert success is True
    assert incident.status == IncidentStatus.CONFIRMED

def test_invalid_status_transition():
    incident = Incident(
        incident_id="INC-001",
        tenant_id="T1",
        city_id="C1",
        site_id="S1",
        incident_type=IncidentType.LANE_BLOCKAGE,
        status=IncidentStatus.CLOSED,
        severity=IncidentSeverity.MEDIUM,
        confidence=0.9,
        detected_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        source_ids=[],
        evidence=[],
        affected_lanes=[],
        affected_signal_groups=[],
        description="Test"
    )
    
    # Invalid transition CLOSED -> CANDIDATE
    success = IncidentStateMachine.transition(incident, IncidentStatus.CANDIDATE, "system")
    assert success is False
    assert incident.status == IncidentStatus.CLOSED
