from datetime import datetime
from src.services.legal.models.schemas import RegulatoryObligation, RegulatoryEvidence
from src.services.legal.engine.compliance import ComplianceEngine

def test_compliance_assessment_insufficient():
    obligation = RegulatoryObligation(
        obligation_id="OBL-001",
        jurisdiction="CITY-A",
        applicable_entity="FACILITY-XYZ",
        requirement="Monthly emissions check"
    )
    
    # Unverified evidence should not count
    evidence = RegulatoryEvidence(
        evidence_id="EV-001",
        source_type="SENSOR",
        observed_at=datetime.utcnow(),
        integrity_status="UNVERIFIED"
    )
    
    engine = ComplianceEngine()
    assessment = engine.assess_compliance(obligation, [evidence])
    
    assert assessment.status == "INSUFFICIENT_EVIDENCE"
    assert len(assessment.evidence_ids) == 0

def test_compliance_assessment_compliant():
    obligation = RegulatoryObligation(
        obligation_id="OBL-002",
        jurisdiction="CITY-B",
        applicable_entity="FACILITY-ABC",
        requirement="Waste check"
    )
    
    evidence = RegulatoryEvidence(
        evidence_id="EV-002",
        source_type="INSPECTION",
        observed_at=datetime.utcnow(),
        integrity_status="VERIFIED"
    )
    
    engine = ComplianceEngine()
    assessment = engine.assess_compliance(obligation, [evidence])
    
    assert assessment.status == "COMPLIANT"
    assert "EV-002" in assessment.evidence_ids
