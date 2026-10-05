from typing import List
from src.services.government.models.schemas import PermitApplication, SpatialPolicy

class SpatialPolicyEngine:
    def evaluate_permit(self, permit: PermitApplication, policies: List[SpatialPolicy]) -> PermitApplication:
        """
        Evaluates a permit application against a set of spatial policies.
        This provides a COMPLIANT / NON_COMPLIANT / REQUIRES_REVIEW classification
        as an aid to the human decision-maker.
        """
        # Simulated spatial policy evaluation
        has_conflict = False
        requires_manual_review = False
        
        for policy in policies:
            if policy.rule_type == "RESTRICTION":
                # Simulated collision logic
                if policy.constraints.get("zone") == permit.location:
                    has_conflict = True
            elif policy.rule_type == "CONDITIONAL":
                requires_manual_review = True
                
        if has_conflict:
            permit.compliance_status = "NON_COMPLIANT"
        elif requires_manual_review:
            permit.compliance_status = "REQUIRES_REVIEW"
        else:
            permit.compliance_status = "COMPLIANT"
            
        return permit
