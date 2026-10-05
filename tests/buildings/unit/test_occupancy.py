import pytest
from src.services.buildings.models.schemas import ZoneOccupancy
from src.services.buildings.engine.occupancy import OccupancyEngine

def test_occupancy_comfort():
    engine = OccupancyEngine()
    
    zone = ZoneOccupancy(
        zone_id="Z1", estimated_occupancy=45, max_capacity=50, comfort_score=1.0
    )
    
    # Perfect conditions, but slightly crowded (90% utilization)
    # The penalty applies if utilization > 0.9, here it's exactly 0.9
    res = engine.evaluate_zone(zone, temperature=22.0, co2_ppm=600)
    assert res.comfort_score == 1.0
    
    # Overcrowded and high CO2
    zone.estimated_occupancy = 48 # 96% utilization -> -0.2
    # temp 26 -> -0.2
    # co2 1100 -> -0.3
    # 1.0 - 0.7 = 0.3
    res2 = engine.evaluate_zone(zone, temperature=26.0, co2_ppm=1100)
    assert res2.comfort_score == pytest.approx(0.3)
