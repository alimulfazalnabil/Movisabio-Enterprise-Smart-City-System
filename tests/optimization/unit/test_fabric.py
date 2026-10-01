import pytest
from datetime import datetime, timezone
from src.services.optimization.models.schemas import OptimizationProblem
from src.services.optimization.engine.fabric import OptimizationFabric

def test_fabric_selects_classical_for_realtime():
    fabric = OptimizationFabric()
    
    problem = OptimizationProblem(
        problem_id="PROB-1",
        tenant_id="T1",
        territory_id="TERR-1",
        problem_type="TRAFFIC_SIGNAL",
        domain="TRAFFIC",
        objective_function="minimize_delay",
        constraints=[],
        problem_size=100,
        data_version="v1",
        created_at=datetime.now(timezone.utc)
    )
    
    # Needs result in 1 second
    job = fabric.queue_job(problem, max_latency_ms=1000)
    
    assert job.backend_type == "CLASSICAL"

def test_fabric_selects_quantum_for_strategic():
    fabric = OptimizationFabric()
    
    problem = OptimizationProblem(
        problem_id="PROB-2",
        tenant_id="T1",
        territory_id="TERR-1",
        problem_type="EV_CHARGING",
        domain="ENERGY",
        objective_function="minimize_cost",
        constraints=[],
        problem_size=500, # Fits on QPU
        data_version="v1",
        created_at=datetime.now(timezone.utc)
    )
    
    # Can wait up to 10 seconds
    job = fabric.queue_job(problem, max_latency_ms=10000)
    
    assert job.backend_type == "QUANTUM"
