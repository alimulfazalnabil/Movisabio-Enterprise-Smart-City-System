from src.platform.application_platform.runtime.container import RuntimeEngine, ApplicationRuntime, RuntimeStatus
from src.platform.application_platform.deployment.deployer import DeploymentEngine, ApplicationDeployment, DeploymentStatus
from src.platform.application_platform.permissions.broker import PermissionBroker
from src.platform.application_platform.functions.executor import FunctionExecutor, AppFunction
from src.platform.application_platform.ui_extensions.registry import UIExtensionRegistry, UIExtension
from src.platform.application_platform.security.quarantine import ApplicationQuarantine

def test_runtime_engine():
    engine = RuntimeEngine()
    runtime = ApplicationRuntime(runtime_id="rt-1", application_id="app-1", instance_id="inst-1", tenant_id="t-1")
    engine.provision_runtime(runtime)
    assert engine.runtimes["rt-1"].status == RuntimeStatus.PROVISIONING
    engine.update_status("rt-1", RuntimeStatus.HEALTHY)
    assert engine.runtimes["rt-1"].status == RuntimeStatus.HEALTHY

def test_deployment_engine():
    engine = DeploymentEngine()
    dep = ApplicationDeployment(deployment_id="dep-1", application_id="app-1", version="1.0.0")
    engine.start_deployment(dep)
    assert engine.deployments["dep-1"].status == DeploymentStatus.PENDING
    engine.advance_deployment("dep-1", DeploymentStatus.ACTIVE)
    assert engine.deployments["dep-1"].status == DeploymentStatus.ACTIVE

def test_permission_broker():
    broker = PermissionBroker()
    assert broker.grant_permissions("app-1", ["traffic.read", "environment.read"]) is True
    assert broker.check_permission("app-1", "traffic.read") is True
    assert broker.check_permission("app-1", "simulation.create") is False
    
    # Restricted permissions
    assert broker.grant_permissions("app-2", ["traffic.control"]) is False

def test_function_executor():
    executor = FunctionExecutor()
    func = AppFunction(function_id="fn-1", application_id="app-1", name="analyze_flood", event_trigger="flood.warning")
    executor.register_function(func)
    result = executor.execute_function("fn-1", {"sensor_val": 1.5})
    assert result["status"] == "success"

def test_ui_extensions():
    registry = UIExtensionRegistry()
    ext = UIExtension(extension_id="ui-1", application_id="app-1", type="widget", name="Traffic Chart", config={})
    registry.register_extension(ext)
    assert len(registry.get_extensions_by_type("widget")) == 1

def test_quarantine_kill_switch():
    runtime_engine = RuntimeEngine()
    runtime_engine.provision_runtime(ApplicationRuntime(runtime_id="rt-1", application_id="app-bad", instance_id="i-1", tenant_id="t-1"))
    runtime_engine.update_status("rt-1", RuntimeStatus.HEALTHY)
    
    quarantine = ApplicationQuarantine(runtime_engine)
    quarantine.kill_switch("app-bad", "malicious activity detected")
    
    assert quarantine.is_quarantined("app-bad") is True
    assert runtime_engine.runtimes["rt-1"].status == RuntimeStatus.SUSPENDED
