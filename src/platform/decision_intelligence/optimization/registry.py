from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class OptimizationProblem(BaseModel):
    problem_id: str
    domain: str
    objective: Dict[str, Any]
    hard_constraints: List[str]
    candidate_solvers: List[str]

class OptimizationRegistry:
    def __init__(self):
        self.problems: Dict[str, OptimizationProblem] = {}
        
    def register_problem(self, problem: OptimizationProblem) -> None:
        self.problems[problem.problem_id] = problem
        
    def solve(self, problem_id: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Routes the problem to the appropriate solver.
        """
        problem = self.problems.get(problem_id)
        if not problem:
            raise ValueError(f"Problem {problem_id} not found")
            
        # Simulated solver execution
        return {
            "solution_id": "sol-1",
            "problem_id": problem_id,
            "selected_solver": problem.candidate_solvers[0] if problem.candidate_solvers else "default",
            "metrics": {"objective_value": 95.5, "compute_time_ms": 120}
        }
