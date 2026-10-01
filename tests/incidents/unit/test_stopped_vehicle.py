import pytest
from src.services.incidents.detection.stopped_vehicle import StoppedVehicleDetector
from src.services.incidents.models.schemas import IncidentType

def test_detects_abnormal_stopped_vehicle():
    detector = StoppedVehicleDetector()
    
    trajectory = {
        'speed': 0.0,
        'duration_stopped': 15,
        'lane_id': 'L1',
        'camera_id': 'CAM-1'
    }
    
    signal = {
        'intersection_id': 'INT-1',
        'active_phase': 'GREEN'
    }
    
    incident = detector.evaluate(trajectory, signal)
    
    assert incident is not None
    assert incident.incident_type == IncidentType.VEHICLE_STOPPED
    assert incident.affected_lanes == ['L1']
    assert len(incident.evidence) == 1

def test_ignores_normal_stopped_vehicle_at_red_light():
    detector = StoppedVehicleDetector()
    
    trajectory = {
        'speed': 0.0,
        'duration_stopped': 45,
        'lane_id': 'L1',
        'camera_id': 'CAM-1'
    }
    
    signal = {
        'intersection_id': 'INT-1',
        'active_phase': 'RED'
    }
    
    incident = detector.evaluate(trajectory, signal)
    
    # Should not flag as incident if they are stopped at a red light
    assert incident is None
