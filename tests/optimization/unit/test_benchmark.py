import pytest
from datetime import datetime, timezone
from src.services.optimization.models.schemas import OptimizationResult
from src.services.optimization.engine.benchmark import BenchmarkEngine

def test_benchmark_quantum_advantage():
    engine = BenchmarkEngine()
    
    classical = OptimizationResult(
        result_id="RES-C", job_id="JOB-C", objective_value=150.0, constraint_violations=0,
        runtime_ms=2000.0, solution_data={}, timestamp=datetime.now(timezone.utc)
    )
    
    quantum = OptimizationResult(
        result_id="RES-Q", job_id="JOB-Q", objective_value=140.0, constraint_violations=0,
        runtime_ms=3500.0, solution_data={}, timestamp=datetime.now(timezone.utc)
    )
    
    record = engine.evaluate_advantage(classical, quantum)
    
    assert record.solution_quality == "QUANTUM_ADVANTAGE"

def test_benchmark_quantum_speedup():
    engine = BenchmarkEngine()
    
    classical = OptimizationResult(
        result_id="RES-C", job_id="JOB-C", objective_value=150.0, constraint_violations=0,
        runtime_ms=5000.0, solution_data={}, timestamp=datetime.now(timezone.utc)
    )
    
    quantum = OptimizationResult(
        result_id="RES-Q", job_id="JOB-Q", objective_value=150.0, constraint_violations=0,
        runtime_ms=1000.0, solution_data={}, timestamp=datetime.now(timezone.utc)
    )
    
    record = engine.evaluate_advantage(classical, quantum)
    
    assert record.solution_quality == "QUANTUM_SPEEDUP"
