import uuid
from datetime import datetime, timezone
from src.services.optimization.models.schemas import OptimizationProblem, OptimizationJob

class OptimizationFabric:
    """
    Selects the appropriate solver backend (Classical, Quantum-Inspired, or Quantum)
    based on problem characteristics, costs, and policies.
    """
    
    def queue_job(self, problem: OptimizationProblem, max_latency_ms: int) -> OptimizationJob:
        """
        Determines the backend based on latency constraints. 
        Classical solvers are prioritized for real-time (latency-critical) problems.
        """
        backend_type = "CLASSICAL"
        solver_id = "OR_TOOLS_MILP"
        
        # If we have time (e.g. strategic planning), we can try quantum-inspired or quantum
        if max_latency_ms > 5000:
            if problem.problem_size > 1000:
                backend_type = "QUANTUM_INSPIRED"
                solver_id = "SIMULATED_ANNEALING"
            else:
                backend_type = "QUANTUM"
                solver_id = "QPU_SOLVER_A"
                
        return OptimizationJob(
            job_id=str(uuid.uuid4()),
            problem_id=problem.problem_id,
            solver_id=solver_id,
            backend_type=backend_type,
            status="QUEUED",
            parameters={"max_time_ms": max_latency_ms},
            created_at=datetime.now(timezone.utc)
        )
