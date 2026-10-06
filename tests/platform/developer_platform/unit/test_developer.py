from src.platform.developer_platform.identity.developer import DeveloperRegistry, Developer, DeveloperStatus
from src.platform.developer_platform.applications.application import ApplicationRegistry, DeveloperApplication, AppStatus
from src.platform.sandbox.developer.sandbox import SandboxManager, SandboxEnvironment

def test_developer_registry():
    registry = DeveloperRegistry()
    dev = Developer(developer_id="dev-1", email="dev@example.com")
    registry.register(dev)
    assert registry.developers["dev-1"].status == DeveloperStatus.REGISTERED
    
    registry.verify("dev-1")
    assert registry.developers["dev-1"].status == DeveloperStatus.VERIFIED

def test_application_registry():
    registry = ApplicationRegistry()
    app = DeveloperApplication(application_id="app-1", developer_id="dev-1", name="My App")
    registry.register_app(app)
    assert registry.applications["app-1"].status == AppStatus.DEVELOPMENT
    
    registry.update_status("app-1", AppStatus.PRODUCTION)
    assert registry.applications["app-1"].status == AppStatus.PRODUCTION

def test_sandbox_provisioning():
    manager = SandboxManager()
    sandbox = SandboxEnvironment(sandbox_id="sb-1", developer_id="dev-1", application_id="app-1", synthetic_tenant_id="t-mock")
    manager.provision_sandbox(sandbox)
    assert manager.sandboxes["sb-1"].active is True
