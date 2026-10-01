import pytest
from datetime import datetime, timezone
from src.services.emergency.models.schemas import EmergencyEvent, Evidence, EmergencyState
from src.services.emergency.engine.correlation import EventCorrelationEngine

def create_base_event() -> EmergencyEvent:
    return EmergencyEvent(
        event_id="E-1",
        tenant_id="T-1",
        event_type="FIRE_CANDIDATE",
        source="SYSTEM",
        source_id="S-1",
        location={"lat": 0, "lon": 0},
        geometry={},
        detected_at=datetime.now(timezone.utc),
        confidence=0.3,
        status=EmergencyState.CANDIDATE,
        created_by="SYSTEM"
    )

def test_correlation_engine_corroborates_evidence():
    engine = EventCorrelationEngine()
    event = create_base_event()
    
    evidence1 = Evidence(
        evidence_id="EV-1",
        event_id="E-1",
        evidence_type="CCTV",
        source="CAM-1",
        timestamp=datetime.now(timezone.utc),
        location={},
        confidence=0.8,
        reference="url"
    )
    
    # 0.3 + (0.8 * 0.3) = 0.54
    updated_event = engine.evaluate_evidence(event, evidence1)
    
    assert updated_event.confidence == pytest.approx(0.54)
    assert updated_event.status == EmergencyState.CORROBORATING

def test_correlation_engine_verifies_on_operator_report():
    engine = EventCorrelationEngine()
    event = create_base_event()
    
    evidence = Evidence(
        evidence_id="EV-2",
        event_id="E-1",
        evidence_type="OPERATOR_REPORT",
        source="OP-1",
        timestamp=datetime.now(timezone.utc),
        location={},
        confidence=1.0,
        reference="call-log"
    )
    
    updated_event = engine.evaluate_evidence(event, evidence)
    
    assert updated_event.status == EmergencyState.VERIFIED
    assert updated_event.verified_at is not None
