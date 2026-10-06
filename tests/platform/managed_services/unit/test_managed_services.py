from src.platform.managed_services.operations.incident import IncidentEngine, OperationsIncident, IncidentSeverity, IncidentStatus
from src.platform.managed_services.noc.health import NOCEngine, InfrastructureHealth, ServiceHealthState
from src.platform.managed_services.ai_ops.drift import AIOpsEngine, AIModelHealth, ModelStatus
from src.platform.managed_services.runbooks.engine import RunbookEngine, RunbookExecution, RunbookStatus

def test_incident_engine():
    engine = IncidentEngine()
    inc = OperationsIncident(
        incident_id="inc-1",
        tenant_id="t-1",
        service_id="s-1",
        severity=IncidentSeverity.P2,
        description="Camera offline"
    )
    engine.create_incident(inc)
    engine.update_status("inc-1", IncidentStatus.CLOSED, root_cause="Power failure")
    assert engine.incidents["inc-1"].status == IncidentStatus.CLOSED
    assert engine.incidents["inc-1"].root_cause == "Power failure"

def test_noc_engine():
    engine = NOCEngine()
    health = InfrastructureHealth(
        component_id="comp-1",
        tenant_id="t-1",
        component_type="NETWORK_LINK"
    )
    engine.register_component(health)
    engine.report_telemetry("comp-1", {"packet_loss": 15.0})
    assert engine.health_records["comp-1"].state == ServiceHealthState.DEGRADED

def test_ai_ops_engine():
    engine = AIOpsEngine()
    model = AIModelHealth(
        model_id="m-1",
        version="v1",
        tenant_id="t-1"
    )
    engine.deploy_model(model)
    engine.evaluate_drift("m-1", drift_score=0.4, current_accuracy=0.75)
    assert engine.models["m-1"].status == ModelStatus.DEGRADED

def test_runbook_engine():
    engine = RunbookEngine()
    exec_record = RunbookExecution(
        execution_id="exec-1",
        runbook_id="rb-restart",
        target_asset_id="cam-1",
        total_steps=2
    )
    engine.trigger_runbook(exec_record)
    engine.log_step("exec-1", "Restarting service")
    assert engine.executions["exec-1"].status == RunbookStatus.EXECUTING
    engine.log_step("exec-1", "Service restarted")
    assert engine.executions["exec-1"].status == RunbookStatus.SUCCESS
