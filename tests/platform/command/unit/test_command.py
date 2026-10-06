from src.platform.command.situation.workspace import WorkspaceManager, SituationWorkspace, SituationStatus
from src.platform.command.operations.task import TaskEngine, OperationalTask, TaskStatus
from src.platform.command.operations.approval import ApprovalEngine, ActionApproval, ApprovalStatus
from src.platform.command.resources.registry import ResourceRegistry, Resource, ResourceStatus
from src.platform.command.session.context import ContextEngine, CommandContext
import pytest

def test_workspace_manager():
    manager = WorkspaceManager()
    ws = SituationWorkspace(situation_id="sit-1", tenant_id="t1", title="Flood", severity="HIGH")
    manager.create_workspace(ws)
    assert manager.workspaces["sit-1"].status == SituationStatus.DETECTED
    
    manager.escalate_situation("sit-1", "CRITICAL")
    assert manager.workspaces["sit-1"].severity == "CRITICAL"
    assert manager.workspaces["sit-1"].status == SituationStatus.ACTIVE

def test_task_engine():
    engine = TaskEngine()
    task = OperationalTask(task_id="task-1", situation_id="sit-1", task_type="inspect", priority="HIGH", organization_id="org-1")
    engine.create_task(task)
    assert engine.tasks["task-1"].status == TaskStatus.PENDING
    
    engine.assign_task("task-1", "user-1")
    assert engine.tasks["task-1"].status == TaskStatus.ASSIGNED
    assert engine.tasks["task-1"].assignee_id == "user-1"

def test_approval_engine():
    engine = ApprovalEngine()
    approval = ActionApproval(approval_id="app-1", situation_id="sit-1", action_type="divert_traffic")
    engine.request_approval(approval)
    assert engine.approvals["app-1"].status == ApprovalStatus.PENDING
    
    engine.process_approval("app-1", "commander-1", ApprovalStatus.APPROVED)
    assert engine.approvals["app-1"].status == ApprovalStatus.APPROVED

def test_resource_registry():
    registry = ResourceRegistry()
    resource = Resource(resource_id="res-1", organization_id="org-1", type="ambulance")
    registry.register_resource(resource)
    
    registry.allocate_resource("res-1", "task-1")
    assert registry.resources["res-1"].status == ResourceStatus.ASSIGNED
    
    with pytest.raises(ValueError):
        registry.allocate_resource("res-1", "task-2")

def test_context_engine():
    engine = ContextEngine()
    context = CommandContext(user_id="u1", organization_id="o1", tenant_id="t1", role="operator", permissions=["view_map", "dispatch"])
    engine.create_session("sess-1", context)
    
    assert engine.authorize_action("sess-1", "dispatch") is True
    assert engine.authorize_action("sess-1", "approve_policy") is False
