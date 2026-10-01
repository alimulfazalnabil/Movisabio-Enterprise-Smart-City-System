import pytest
from src.services.territory.models.schemas import Parcel
from src.services.territory.engine.accessibility import InfrastructureAccessibilityEngine

def test_accessibility_gaps():
    engine = InfrastructureAccessibilityEngine()
    
    parcel = Parcel(
        parcel_id="P-1",
        tenant_id="T1",
        geometry={},
        area_sqm=500.0,
        land_use="RESIDENTIAL",
        land_cover="BUILT",
        development_status="DEVELOPED",
        infrastructure_access={"HOSPITAL": "HIGH", "TRANSIT": "LIMITED"},
        risk_exposure={}
    )
    
    gaps = engine.evaluate_gaps(parcel, ["HOSPITAL", "TRANSIT", "WASTE"])
    
    assert gaps["HOSPITAL"] == "ADEQUATE"
    assert gaps["TRANSIT"] == "WARNING"
    assert gaps["WASTE"] == "CRITICAL_GAP"
