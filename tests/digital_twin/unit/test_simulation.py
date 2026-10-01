import pytest
from src.services.digital_twin.engine.simulation import SimulationOrchestrator

def test_simulation_orchestrator():
    orchestrator = SimulationOrchestrator()
    
    job = orchestrator.queue_job("SCEN-1", "v1.0", "SUMO", {"target": "INT-1"})
    
    assert job.status == "QUEUED"
    assert job.simulation_engine == "SUMO"
    
    completed_job = orchestrator.execute_mock_job(job)
    
    assert completed_job.status == "COMPLETED"
    assert completed_job.result_data["avg_travel_time_sec"] == 300
