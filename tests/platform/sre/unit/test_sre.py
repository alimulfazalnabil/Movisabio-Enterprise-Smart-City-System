from datetime import datetime, timezone
from src.platform.sre.slo.monitor import SLO, ErrorBudget
from src.platform.incident_management.command import IncidentCommand

def test_error_budget():
    slo = SLO(service_id="svc-1", indicator="availability", target=0.99, window="30d")
    budget = ErrorBudget(slo)
    
    # Send 100 requests, 1 fails
    for _ in range(99):
        budget.record_request(success=True)
    budget.record_request(success=False)
    
    assert budget.is_budget_exhausted() is False
    
    # Send another failure, dropping rate to 98% (below 99% target)
    budget.record_request(success=False)
    budget.record_request(success=False) # 99 success, 3 fails = 102 total. 99/102 = 0.97
    
    assert budget.is_budget_exhausted() is True

def test_incident_command():
    cmd = IncidentCommand()
    ts = datetime.now(timezone.utc)
    
    inc = cmd.declare_incident("svc-1", "P2", ts)
    assert inc.status == "DETECTED"
    assert inc.severity == "P2"
    
    cmd.escalate(inc.incident_id, "P1")
    
    assert cmd.incidents[0].severity == "P1"
    
    ts_resolved = datetime.now(timezone.utc)
    cmd.resolve(inc.incident_id, ts_resolved)
    
    assert cmd.incidents[0].status == "RESOLVED"
    assert cmd.incidents[0].resolved_at == ts_resolved
