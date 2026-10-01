import uuid
from datetime import datetime, timezone
from typing import List
from src.services.optimization.models.schemas import BenchmarkRecord, OptimizationResult

class BenchmarkEngine:
    """
    Evaluates whether a quantum backend actually provides an advantage over classical baselines.
    """
    
    def evaluate_advantage(self, classical_result: OptimizationResult, quantum_result: OptimizationResult) -> BenchmarkRecord:
        """
        Creates a benchmark comparing classical vs quantum. 
        Focuses on the quantum run but assesses 'solution_quality' relative to classical.
        (Assuming minimization problem)
        """
        quality = "INFERIOR"
        
        # Did it find a better objective?
        if quantum_result.objective_value < classical_result.objective_value:
            quality = "QUANTUM_ADVANTAGE"
        # Or did it find the same objective but faster?
        elif quantum_result.objective_value == classical_result.objective_value and quantum_result.runtime_ms < classical_result.runtime_ms:
            quality = "QUANTUM_SPEEDUP"
            
        return BenchmarkRecord(
            benchmark_id=str(uuid.uuid4()),
            problem_id=quantum_result.job_id, # Simplified for mock
            solver_id="QUANTUM_VS_CLASSICAL",
            backend_type="COMPARISON",
            objective_value=quantum_result.objective_value,
            runtime_ms=quantum_result.runtime_ms,
            compute_cost=15.0, # Mock cost
            solution_quality=quality,
            timestamp=datetime.now(timezone.utc)
        )
