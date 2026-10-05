from typing import List, Callable, Any, Dict

class SagaStep:
    def __init__(self, name: str, execute_fn: Callable, compensate_fn: Callable):
        self.name = name
        self.execute = execute_fn
        self.compensate = compensate_fn
        self.status = "PENDING"

class SagaCoordinator:
    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps: List[SagaStep] = []
        
    def add_step(self, step: SagaStep) -> None:
        self.steps.append(step)
        
    async def execute(self, context: Dict[str, Any]) -> bool:
        executed_steps = []
        for step in self.steps:
            try:
                step.status = "EXECUTING"
                success = await step.execute(context)
                if not success:
                    raise Exception(f"Step {step.name} failed")
                step.status = "COMPLETED"
                executed_steps.append(step)
            except Exception as e:
                step.status = "FAILED"
                await self._compensate(executed_steps, context)
                return False
        return True
        
    async def _compensate(self, steps: List[SagaStep], context: Dict[str, Any]) -> None:
        # Compensate in reverse order
        for step in reversed(steps):
            try:
                step.status = "COMPENSATING"
                await step.compensate(context)
                step.status = "COMPENSATED"
            except Exception:
                step.status = "COMPENSATION_FAILED"
                # Log critical failure
