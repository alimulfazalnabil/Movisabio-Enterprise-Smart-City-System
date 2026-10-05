import pytest
from src.services.demand.models.schemas import ActivityZone
from src.services.demand.engine.forecasting import DemandForecaster

def test_demand_forecasting():
    forecaster = DemandForecaster()
    
    zone = ActivityZone(
        zone_id="Z1",
        activity_types=["COMMERCIAL"],
        population_estimate=1000,
        employment_estimate=5000,
        activity_intensity_profile={"8": 1.5, "12": 1.0, "3": 0.1}
    )
    
    # 1000*1.5 + 5000*2 = 11500 base trips. 
    # At 8 AM (intensity 1.5): (11500 * 1.5) / 24 = 718
    vol_8, conf_8 = forecaster.forecast_zone_generation(zone, 8)
    assert vol_8 == 718
    assert conf_8 == 0.85
    
    # At 3 AM (intensity 0.1): (11500 * 0.1) / 24 = 47
    vol_3, conf_3 = forecaster.forecast_zone_generation(zone, 3)
    assert vol_3 == 47
    assert conf_3 == 0.70 # Lower confidence for extreme off-peak
