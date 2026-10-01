import pytest
from datetime import datetime, timedelta, timezone
from src.services.citizen.models.schemas import CitizenServiceRequest, ServiceCatalogEntry, RequestStatus
from src.services.citizen.engine.sla import SLAEngine

def test_sla_target_calculation():
    engine = SLAEngine()
    now = datetime.now(timezone.utc)
    
    req = CitizenServiceRequest(
        request_id="R-1",
        tenant_id="T-1",
        citizen_id="C-1",
        service_id="S-1",
        category="CAT",
        subcategory="SUB",
        title="Test",
        description="Test",
        location={},
        geometry={},
        address="Test",
        created_at=now,
        updated_at=now
    )
    
    catalog = [
        ServiceCatalogEntry(
            service_id="S-1",
            name="Test",
            description="Test",
            department="DEPT",
            category="CAT",
            eligibility="ALL",
            required_information=[],
            optional_information=[],
            sla_target_hours=48.0,
            priority_rules={},
            workflow="STD",
            status_visibility="PUBLIC"
        )
    ]
    
    updated_req = engine.apply_sla(req, catalog)
    
    expected_due = now + timedelta(hours=48)
    assert updated_req.sla_due_at == expected_due

def test_sla_breach_detection():
    engine = SLAEngine()
    now = datetime.now(timezone.utc)
    
    req = CitizenServiceRequest(
        request_id="R-2",
        tenant_id="T-1",
        citizen_id="C-1",
        service_id="S-1",
        category="CAT",
        subcategory="SUB",
        title="Test",
        description="Test",
        location={},
        geometry={},
        address="Test",
        created_at=now - timedelta(hours=50),
        updated_at=now,
        sla_due_at=now - timedelta(hours=2), # Due 2 hours ago
        status=RequestStatus.IN_PROGRESS
    )
    
    assert engine.check_sla_breach(req) is True

def test_sla_ignores_resolved_tickets():
    engine = SLAEngine()
    now = datetime.now(timezone.utc)
    
    req = CitizenServiceRequest(
        request_id="R-3",
        tenant_id="T-1",
        citizen_id="C-1",
        service_id="S-1",
        category="CAT",
        subcategory="SUB",
        title="Test",
        description="Test",
        location={},
        geometry={},
        address="Test",
        created_at=now - timedelta(hours=50),
        updated_at=now,
        sla_due_at=now - timedelta(hours=2), 
        status=RequestStatus.RESOLVED # It's resolved, so not currently breaching
    )
    
    assert engine.check_sla_breach(req) is False
