from datetime import datetime
from src.services.government.models.schemas import GovernmentCase, PermitApplication, SpatialPolicy
from src.services.government.engine.workflow import WorkflowEngine
from src.services.government.engine.policy import SpatialPolicyEngine

def test_workflow_transition():
    case = GovernmentCase(
        case_id="CASE-001",
        case_type="INFRASTRUCTURE_REPAIR",
        status="SUBMITTED",
        assigned_department="PUBLIC_WORKS",
        created_at=datetime.utcnow()
    )
    engine = WorkflowEngine()
    
    case = engine.transition_case(case, "start_review")
    assert case.status == "UNDER_REVIEW"
    
    case = engine.transition_case(case, "approve")
    assert case.status == "APPROVED"
    
    # Invalid transition (APPROVED -> approve) should not change status
    case = engine.transition_case(case, "approve")
    assert case.status == "APPROVED"

def test_spatial_policy_evaluation():
    permit = PermitApplication(
        permit_id="PERMIT-001",
        applicant_id="USER-123",
        permit_type="CONSTRUCTION",
        location="ZONE-A",
        status="SUBMITTED"
    )
    
    policy_compliant = SpatialPolicy(
        policy_id="POL-01",
        jurisdiction="CITY",
        rule_type="RESTRICTION",
        constraints={"zone": "ZONE-B"}
    )
    
    policy_conflict = SpatialPolicy(
        policy_id="POL-02",
        jurisdiction="CITY",
        rule_type="RESTRICTION",
        constraints={"zone": "ZONE-A"}
    )
    
    engine = SpatialPolicyEngine()
    
    # Test compliant
    result_compliant = engine.evaluate_permit(permit, [policy_compliant])
    assert result_compliant.compliance_status == "COMPLIANT"
    
    # Test non-compliant
    result_conflict = engine.evaluate_permit(permit, [policy_compliant, policy_conflict])
    assert result_conflict.compliance_status == "NON_COMPLIANT"
