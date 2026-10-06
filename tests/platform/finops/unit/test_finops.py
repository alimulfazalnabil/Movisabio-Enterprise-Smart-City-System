from src.platform.finops.usage_metering.ledger import UsageLedger
from src.platform.finops.cost_engine.calculator import CostCalculator
from src.platform.finops.budgets.enforcer import Budget, BudgetEnforcer

def test_usage_and_cost():
    ledger = UsageLedger()
    calc = CostCalculator()
    
    ledger.record_usage("tenant-1", "traffic-cv", "vehicle_detection", "gpu_seconds", 10000, "seconds")
    total_usage = ledger.get_total_usage("tenant-1", "gpu_seconds")
    
    assert total_usage == 10000
    
    cost = calc.calculate_cost("gpu_seconds", total_usage)
    assert cost == 4.0 # 10000 * 0.0004

def test_budget_enforcement():
    enforcer = BudgetEnforcer()
    budget = Budget(
        tenant_id="tenant-1",
        monthly_limit=100.0,
        warning_threshold=70.0,
        critical_threshold=90.0
    )
    enforcer.set_budget(budget)
    
    state = enforcer.record_spend("tenant-1", 50.0)
    assert state == "ACTIVE"
    
    state = enforcer.record_spend("tenant-1", 25.0) # 75 total
    assert state == "WARNING"
    
    state = enforcer.record_spend("tenant-1", 20.0) # 95 total
    assert state == "CRITICAL"
    
    state = enforcer.record_spend("tenant-1", 10.0) # 105 total
    assert state == "EXCEEDED"
    
    # Non-critical workload blocked
    assert enforcer.check_authorization("tenant-1", is_safety_critical=False) is False
    
    # Safety critical workload allowed
    assert enforcer.check_authorization("tenant-1", is_safety_critical=True) is True
