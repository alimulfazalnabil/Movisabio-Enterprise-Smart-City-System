import pytest
from datetime import datetime, timezone
from src.services.climate.models.schemas import ClimateHazard
from src.services.climate.engine.risk import ClimateRiskEngine

def test_climate_risk_exposure():
    engine = ClimateRiskEngine()
    
    hazard = ClimateHazard(
        hazard_id="H-1",
        hazard_type="FLOOD",
        geometry={"zone": "NORTH"},
        intensity_score=8.5,
        probability=0.9,
        valid_time=datetime.now(timezone.utc)
    )
    
    assets = [
        {"asset_id": "A1", "zone": "NORTH"},
        {"asset_id": "A2", "zone": "SOUTH"},
        {"asset_id": "A3", "zone": "NORTH"}
    ]
    
    exposure = engine.calculate_exposure(hazard, assets)
    
    assert "A1" in exposure.exposed_asset_ids
    assert "A3" in exposure.exposed_asset_ids
    assert "A2" not in exposure.exposed_asset_ids
    assert exposure.vulnerability_score == pytest.approx(2/3)
    assert exposure.potential_impact_category == "HIGH"
