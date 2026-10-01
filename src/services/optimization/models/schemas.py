from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class OptimizationProblem(BaseModel):
    problem_id: str
    tenant_id: str
    territory_id: str
    problem_type: str # e.g. TRAFFIC_SIGNAL_OPTIMIZATION, WASTE_COLLECTION_ROUTING
    domain: str
    objective_function: str
    constraints: List[str]
    problem_size: int
    data_version: str
    created_at: datetime

class OptimizationJob(BaseModel):
    job_id: str
    problem_id: str
    solver_id: str
    backend_type: str # CLASSICAL, QUANTUM_INSPIRED, QUANTUM
    status: str # QUEUED, SUBMITTED, RUNNING, COMPLETED, FAILED
    parameters: Dict[str, Any]
    created_at: datetime

class OptimizationResult(BaseModel):
    result_id: str
    job_id: str
    objective_value: float
    constraint_violations: int
    runtime_ms: float
    solution_data: Dict[str, Any]
    timestamp: datetime

class BenchmarkRecord(BaseModel):
    benchmark_id: str
    problem_id: str
    solver_id: str
    backend_type: str
    objective_value: float
    runtime_ms: float
    compute_cost: float
    solution_quality: str
    timestamp: datetime
