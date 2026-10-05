import pytest
from src.services.logistics.models.schemas import LogisticsFacility
from src.services.logistics.engine.facility import FacilityIntelligenceEngine

def test_facility_status_evaluation():
    engine = FacilityIntelligenceEngine()
    
    fac1 = LogisticsFacility(
        facility_id="F1", facility_type="WAREHOUSE", capacity=1000, 
        current_load=960, truck_queue_length=5, status="NORMAL", location="ZONE_A"
    )
    assert engine.evaluate_facility_status(fac1) == "CONGESTED" # > 95% utilization
    
    fac2 = LogisticsFacility(
        facility_id="F2", facility_type="WAREHOUSE", capacity=1000, 
        current_load=800, truck_queue_length=25, status="NORMAL", location="ZONE_A"
    )
    assert engine.evaluate_facility_status(fac2) == "CONGESTED" # > 20 trucks in queue
    
    fac3 = LogisticsFacility(
        facility_id="F3", facility_type="WAREHOUSE", capacity=1000, 
        current_load=860, truck_queue_length=5, status="NORMAL", location="ZONE_A"
    )
    assert engine.evaluate_facility_status(fac3) == "HIGH_LOAD" # > 85% utilization
