import pytest
from datetime import datetime, timezone
from src.services.emergency.models.schemas import EmergencyEvent, EmergencyResource, EmergencyState
from src.services.emergency.engine.dispatch import DispatchEngine

def test_dispatch_engine_ignores_candidates():
    engine = DispatchEngine()
    
    event = EmergencyEvent(
        event_id="E-1",
        tenant_id="T-1",
        event_type="FIRE_CANDIDATE",
        source="SYSTEM",
        source_id="S-1",
        location={},
        geometry={},
        detected_at=datetime.now(timezone.utc),
        confidence=0.5,
        status=EmergencyState.CANDIDATE,
        created_by="SYSTEM"
    )
    
    resources = [
        EmergencyResource(
            resource_id="R-1",
            tenant_id="T-1",
            resource_type="FIRE_TRUCK",
            organization_id="FD-1",
            location={},
            availability="HIGH",
            capability=["FIRE_SUPPRESSION"],
            status="AVAILABLE"
        )
    ]
    
    recommendation = engine.recommend_resources(event, resources, "FIRE_SUPPRESSION")
    
    assert recommendation is None

def test_dispatch_engine_finds_resource_for_verified_event():
    engine = DispatchEngine()
    
    event = EmergencyEvent(
        event_id="E-1",
        tenant_id="T-1",
        event_type="STRUCTURE_FIRE",
        source="SYSTEM",
        source_id="S-1",
        location={},
        geometry={},
        detected_at=datetime.now(timezone.utc),
        confidence=1.0,
        status=EmergencyState.VERIFIED,
        created_by="SYSTEM"
    )
    
    resources = [
        EmergencyResource(
            resource_id="R-1",
            tenant_id="T-1",
            resource_type="AMBULANCE",
            organization_id="MED-1",
            location={},
            availability="HIGH",
            capability=["MEDICAL"],
            status="AVAILABLE"
        ),
        EmergencyResource(
            resource_id="R-2",
            tenant_id="T-1",
            resource_type="FIRE_TRUCK",
            organization_id="FD-1",
            location={},
            availability="HIGH",
            capability=["FIRE_SUPPRESSION"],
            status="AVAILABLE"
        )
    ]
    
    recommendation = engine.recommend_resources(event, resources, "FIRE_SUPPRESSION")
    
    assert recommendation is not None
    assert recommendation.resource_id == "R-2"
