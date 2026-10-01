import pytest
from src.services.territory.models.schemas import Parcel, ConstraintLevel
from src.services.territory.engine.constraint import TerritorialConstraintEngine

def test_constraint_engine_detects_flood_risk():
    engine = TerritorialConstraintEngine()
    
    parcel = Parcel(
        parcel_id="P-1",
        tenant_id="T1",
        geometry={},
        area_sqm=500.0,
        land_use="RESIDENTIAL",
        land_cover="BUILT",
        development_status="DEVELOPED",
        infrastructure_access={},
        risk_exposure={"FLOOD_RISK": "HIGH"}
    )
    
    constraints = engine.evaluate_parcel(parcel)
    
    assert len(constraints) == 1
    assert constraints[0].constraint_type == "FLOOD_RISK"
    assert constraints[0].level == ConstraintLevel.CONSTRAINT
