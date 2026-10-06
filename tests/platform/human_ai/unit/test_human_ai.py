from src.platform.human_ai.oversight.oversight_engine import OversightEngine, OverrideEvent
from src.platform.ai_governance.policy_engine.policy_engine import PolicyEngine, GovernancePolicy
from src.platform.ai_governance.evidence.decision_provenance import ProvenanceEngine, DecisionEvidence
from src.platform.governance.incidents.ai_incident import AIIncidentManager, AIIncident, AIIncidentSeverity, AIIncidentStatus

def test_oversight_engine():
    engine = OversightEngine()
    override = OverrideEvent(
        override_id="ovr-1",
        action_id="act-42",
        overriding_user="admin",
        reason="Agent proposed excessive scale",
        new_action="SCALE_2_NODES"
    )
    engine.record_override(override)
    
    overrides = engine.get_overrides_for_action("act-42")
    assert len(overrides) == 1
    assert overrides[0].new_action == "SCALE_2_NODES"

def test_policy_engine():
    engine = PolicyEngine()
    policy = GovernancePolicy(
        policy_id="pol-infra",
        name="Infra Scaling",
        requires_human_approval=True,
        budget_limit=1000.0,
        risk_class="MEDIUM"
    )
    engine.add_policy(policy)
    
    # Over budget and High risk
    result = engine.evaluate_action("pol-infra", proposed_budget=1500.0, action_risk="HIGH")
    assert result["approved"] is False
    assert len(result["reasons"]) == 1
    
    # Within limits
    result = engine.evaluate_action("pol-infra", proposed_budget=500.0, action_risk="LOW")
    assert result["approved"] is True
    assert result["requires_human"] is True

def test_provenance_engine():
    engine = ProvenanceEngine()
    evidence = DecisionEvidence(
        decision_id="dec-1",
        agent_id="infra-agent",
        model_version="v2.1",
        confidence=0.85,
        policy_applied="pol-infra"
    )
    engine.record_evidence(evidence)
    
    replay = engine.replay_decision("dec-1")
    assert replay.agent_id == "infra-agent"
    assert replay.confidence == 0.85

def test_ai_incident_manager():
    manager = AIIncidentManager()
    incident = AIIncident(
        incident_id="inc-1",
        decision_id="dec-1",
        severity=AIIncidentSeverity.AI_P1,
        description="Agent hallucinated budget constraint"
    )
    manager.report_incident(incident)
    
    resolved = manager.resolve_incident("inc-1", "LLM context window overflow")
    assert resolved.status == AIIncidentStatus.REMEDIATED
    assert resolved.root_cause == "LLM context window overflow"
