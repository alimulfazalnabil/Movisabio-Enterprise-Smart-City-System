from typing import Dict, Any, List

class GlobalGovernanceEngine:
    """
    B46 - Global Data Governance, Compliance & Responsible AI
    Enforces data sovereignty, AI risk, and policy-as-code rules across the platform.
    """

    def evaluate_cross_border_transfer(self, data_asset: Dict[str, Any], target_jurisdiction: str) -> Dict[str, Any]:
        """
        B46.10 - Cross-Border Data Governance
        Determines if a data asset can be legally transferred or federated to a new jurisdiction.
        """
        classification = data_asset.get("classification", "PUBLIC")
        residency = data_asset.get("residency", "GLOBAL")
        source_jurisdiction = data_asset.get("jurisdiction", "UNKNOWN")
        
        is_allowed = True
        reason = "Transfer Allowed"
        
        if classification == "SOVEREIGN" and source_jurisdiction != target_jurisdiction:
             is_allowed = False
             reason = f"SOVEREIGN data cannot leave {source_jurisdiction} without explicit exception."
             
        elif residency == "EU_ONLY" and target_jurisdiction not in ["EU", "EEA"]:
             is_allowed = False
             reason = "Data residency policy restricts export outside EU."
             
        return {
            "transfer_allowed": is_allowed,
            "source_jurisdiction": source_jurisdiction,
            "target_jurisdiction": target_jurisdiction,
            "reason": reason,
            "required_controls": ["TLS 1.3", "Data Contract Logging"] if is_allowed else []
        }

    def validate_ai_action_safety(self, agent_id: str, proposed_action: str, ai_risk_level: str) -> Dict[str, Any]:
        """
        B46.14 - AI Risk Classification & B46.31 - Governance + Agent Architecture
        Ensures AI agents do not exceed their authorized risk boundaries.
        """
        requires_human = False
        allowed = True
        
        if ai_risk_level in ["AI-R4", "AI-R5"]:
             requires_human = True
             allowed = False # Must go through approval queue
             
        if "physical_system" in proposed_action and ai_risk_level != "AI-R5":
             allowed = False
             reason = "Only AI-R5 certified models may propose physical system changes."
        else:
             reason = "Action falls within acceptable risk boundaries." if allowed else "Human approval required for high-risk actions."
             
        return {
            "agent_id": agent_id,
            "proposed_action": proposed_action,
            "action_authorized": allowed,
            "requires_human_approval": requires_human,
            "reason": reason
        }

    def evaluate_purpose_limitation(self, data_purpose: str, requested_purpose: str) -> bool:
        """
        B46.7 - Purpose Limitation
        Verifies that data is only used for its legally collected purpose.
        """
        # In a real system, this would evaluate a purpose ontology or ML semantic matching.
        # For this skeleton, we enforce exact or subset matching.
        if data_purpose == "ANY": return True
        return requested_purpose in data_purpose or requested_purpose == data_purpose
