from typing import List
from src.services.legal.models.schemas import RegulatoryObligation, RegulatoryEvidence, ComplianceAssessment

class ComplianceEngine:
    def assess_compliance(self, obligation: RegulatoryObligation, evidence_list: List[RegulatoryEvidence]) -> ComplianceAssessment:
        """
        Evaluates an obligation against provided evidence.
        """
        valid_evidence = [e for e in evidence_list if e.integrity_status == "VERIFIED"]
        
        status = "INSUFFICIENT_EVIDENCE"
        if len(valid_evidence) > 0:
            # Simplistic check: If there is verified evidence, we mark it as compliant.
            # In a real scenario, this would use a rule engine on the evidence payload.
            status = "COMPLIANT"
            
        return ComplianceAssessment(
            assessment_id=f"ASSESS-{obligation.obligation_id}",
            obligation_id=obligation.obligation_id,
            entity_id=obligation.applicable_entity,
            status=status,
            evidence_ids=[e.evidence_id for e in valid_evidence]
        )
