import pytest
from datetime import datetime, timezone
from src.services.citizen.models.schemas import CitizenServiceRequest, ServiceCatalogEntry, RequestStatus
from src.services.citizen.engine.triage import RequestTriageEngine

def create_request(req_id: str, category: str, lat: float, lon: float, status: RequestStatus) -> CitizenServiceRequest:
    return CitizenServiceRequest(
        request_id=req_id,
        tenant_id="T-1",
        citizen_id="C-1",
        service_id="S-1",
        category=category,
        subcategory="test",
        title="Test",
        description="Test",
        location={"lat": lat, "lon": lon},
        geometry={},
        address="Test",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        status=status
    )

def test_triage_detects_duplicate():
    engine = RequestTriageEngine()
    
    req1 = create_request("R-1", "FLOODING", 23.78, 90.40, RequestStatus.IN_PROGRESS)
    req2 = create_request("R-2", "FLOODING", 23.7801, 90.4001, RequestStatus.SUBMITTED)
    
    dup_id = engine.detect_duplicate(req2, [req1], distance_threshold_deg=0.001)
    
    assert dup_id == "R-1"

def test_triage_ignores_closed_duplicates():
    engine = RequestTriageEngine()
    
    req1 = create_request("R-1", "FLOODING", 23.78, 90.40, RequestStatus.RESOLVED)
    req2 = create_request("R-2", "FLOODING", 23.7801, 90.4001, RequestStatus.SUBMITTED)
    
    dup_id = engine.detect_duplicate(req2, [req1], distance_threshold_deg=0.001)
    
    assert dup_id is None

def test_triage_routing():
    engine = RequestTriageEngine()
    
    catalog = [
        ServiceCatalogEntry(
            service_id="S-1",
            name="Flood Reporting",
            description="Report floods",
            department="DRAINAGE_DEPT",
            category="ENVIRONMENT",
            eligibility="ALL",
            required_information=[],
            optional_information=[],
            sla_target_hours=24.0,
            priority_rules={},
            workflow="STD",
            status_visibility="PUBLIC"
        )
    ]
    
    req = create_request("R-3", "FLOODING", 23.78, 90.40, RequestStatus.SUBMITTED)
    routed = engine.route_request(req, catalog)
    
    assert routed.assigned_department == "DRAINAGE_DEPT"
    assert routed.status == RequestStatus.TRIAGED
