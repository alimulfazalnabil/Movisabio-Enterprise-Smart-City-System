import uuid
from datetime import datetime, timezone
from src.services.digital_twin.models.schemas import SimulationJob

class SimulationOrchestrator:
    """
    Manages multi-domain simulation jobs.
    """
    
    def queue_job(self, scenario_id: str, baseline_twin_version: str, engine: str, parameters: dict) -> SimulationJob:
        return SimulationJob(
            job_id=str(uuid.uuid4()),
            scenario_id=scenario_id,
            baseline_twin_version=baseline_twin_version,
            simulation_engine=engine,
            engine_version="1.0",
            parameters=parameters,
            status="QUEUED",
            created_at=datetime.now(timezone.utc)
        )
        
    def execute_mock_job(self, job: SimulationJob) -> SimulationJob:
        """
        Mocks the execution of a job. Real implementation would send to async worker queue.
        """
        job.status = "COMPLETED"
        if job.simulation_engine == "SUMO":
            job.result_data = {"avg_travel_time_sec": 300, "queue_length_m": 50}
        elif job.simulation_engine == "FLOOD":
            job.result_data = {"exposed_buildings": 12, "peak_water_level_m": 1.2}
        else:
            job.result_data = {"status": "success"}
            
        return job
