import pytest
from src.platform.decision.engine import DecisionEngine
from src.platform.workflow.saga.coordinator import SagaCoordinator, SagaStep

def test_decision_arbitration():
    candidates = [
        {"id": "c1", "category": "OPTIMIZATION", "action": "extend_green"},
        {"id": "c2", "category": "EMERGENCY", "action": "force_green_for_ambulance"}
    ]
    
    decision = DecisionEngine.arbitrate(candidates, [])
    assert decision is not None
    assert decision["selected_candidate"]["id"] == "c2" # Emergency wins over Optimization

@pytest.mark.asyncio
async def test_saga_success():
    context = {}
    
    async def exec_fn(ctx):
        ctx["executed"] = True
        return True
        
    async def comp_fn(ctx):
        ctx["compensated"] = True
        
    step = SagaStep("test_step", exec_fn, comp_fn)
    coordinator = SagaCoordinator("saga-1")
    coordinator.add_step(step)
    
    success = await coordinator.execute(context)
    assert success is True
    assert context.get("executed") is True
    assert context.get("compensated") is None
    assert step.status == "COMPLETED"

@pytest.mark.asyncio
async def test_saga_compensation():
    context = {}
    
    async def exec_pass(ctx):
        ctx["step1_done"] = True
        return True
        
    async def comp_pass(ctx):
        ctx["step1_compensated"] = True
        
    async def exec_fail(ctx):
        return False # This fails
        
    async def comp_fail(ctx):
        pass
        
    step1 = SagaStep("step1", exec_pass, comp_pass)
    step2 = SagaStep("step2", exec_fail, comp_fail)
    
    coordinator = SagaCoordinator("saga-2")
    coordinator.add_step(step1)
    coordinator.add_step(step2)
    
    success = await coordinator.execute(context)
    assert success is False
    assert context.get("step1_done") is True
    # Verify compensation ran for step 1
    assert context.get("step1_compensated") is True
    assert step1.status == "COMPENSATED"
    assert step2.status == "FAILED"
