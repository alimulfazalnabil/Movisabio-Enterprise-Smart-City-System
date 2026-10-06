from datetime import datetime, timezone
from src.platform.experience.bff.context import SessionContext
from src.platform.experience.workspaces.manager import WorkspaceManager, Workspace, Widget
from src.platform.experience.approvals.center import ApprovalCenter, ApprovalRequest
from src.platform.experience.ai_assistant.explainability import Assistant, ExplainableRecommendation

def test_session_context():
    ctx = SessionContext(
        user_id="u1",
        tenant_id="t1",
        organization_id="o1",
        role="TRAFFIC_OPERATOR",
        jurisdiction_id="DE",
        region_id="eu-de-01",
        permissions=["read:traffic", "execute:signal"],
        data_classification_scope=["OPERATIONAL"]
    )
    
    assert ctx.can_access("execute:signal") is True
    assert ctx.can_access("admin:users") is False

def test_workspace_manager():
    mgr = WorkspaceManager()
    
    w = Workspace(
        workspace_id="ws-1",
        user_id="u1",
        tenant_id="t1",
        name="Morning Peak",
        role_target="TRAFFIC_OPERATOR",
        widgets=[
            Widget(widget_id="wid-1", type="MAP", configuration={"layers": ["traffic"]})
        ],
        created_at=datetime.now(timezone.utc)
    )
    
    mgr.create_workspace(w)
    
    workspaces = mgr.get_user_workspaces("u1", "t1")
    assert len(workspaces) == 1
    assert workspaces[0].name == "Morning Peak"

def test_approval_center():
    center = ApprovalCenter()
    
    req = ApprovalRequest(
        request_id="req-1",
        tenant_id="t1",
        requester_id="u1",
        action_type="UPDATE_SIGNAL_TIMING",
        target_resource="intersection-104",
        risk_level="HIGH",
        evidence="AI Prediction + Queue Length > 100m",
        created_at=datetime.now(timezone.utc)
    )
    
    center.submit_request(req)
    assert center.requests["req-1"].status == "PENDING"
    
    center.resolve_request("req-1", "u2", "APPROVED")
    assert center.requests["req-1"].status == "APPROVED"

def test_explainability():
    assistant = Assistant()
    
    rec = ExplainableRecommendation(
        recommendation_id="rec-1",
        problem_statement="Severe congestion on Corridor A",
        action_recommended="Apply Phase Allocation Plan B",
        confidence_score=0.88,
        evidence_sources=["Camera 42", "Queue Model"],
        safety_status="PASSED",
        policy_reference="Traffic Policy v4"
    )
    
    text = assistant.format_explanation(rec)
    assert "RECOMMENDATION: Apply Phase Allocation Plan B" in text
    assert "SAFETY: PASSED" in text
