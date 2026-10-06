from datetime import datetime, timezone
from src.platform.governance.registry.jurisdiction import GovernanceRegistry, Jurisdiction, Requirement
from src.platform.governance.risk.register import RiskRegister, Risk
from src.platform.governance.evidence.fabric import EvidenceStore

def test_jurisdiction_registry():
    reg = GovernanceRegistry()
    
    de = Jurisdiction(
        jurisdiction_id="DE",
        name="Germany",
        type="COUNTRY",
        country_code="DE"
    )
    reg.add_jurisdiction(de)
    
    req = Requirement(
        requirement_id="GDPR-01",
        jurisdiction_id="DE",
        source="GDPR",
        category="privacy",
        applies_to=["cctv"],
        controls=["encryption", "retention_30d"]
    )
    reg.add_requirement(req)
    
    reqs = reg.get_requirements_for_system("cctv", "DE")
    assert len(reqs) == 1
    assert reqs[0].requirement_id == "GDPR-01"

def test_risk_register():
    reg = RiskRegister()
    
    r = Risk(
        risk_id="r-1",
        tenant_id="t-1",
        category="AI",
        title="Stale Command",
        description="AI sends stale command to controller",
        asset_id="traffic-ai",
        likelihood=3,
        impact=5,
        created_at=datetime.now(timezone.utc)
    )
    
    reg.log_risk(r)
    assert r.inherent_risk == 15
    
    reg.treat_risk("r-1", new_likelihood=1, new_impact=5, treatment_plan="TTL Fencing")
    assert r.residual_risk == 5
    assert r.status == "MITIGATING"

def test_evidence_fabric():
    store = EvidenceStore()
    
    eid = store.submit_evidence(
        control_id="encryption",
        source_system="ci-cd",
        artifact_uri="s3://evidence/enc-test",
        content=b"test passed"
    )
    
    assert eid in store.evidence
    evd = store.evidence[eid]
    assert evd.verification_status == "PENDING"
    
    store.verify_evidence(eid)
    assert evd.verification_status == "VERIFIED"
