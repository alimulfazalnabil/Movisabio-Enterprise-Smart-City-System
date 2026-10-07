from typing import Dict, Any, List

class TrustIntelligenceEngine:
    """
    B26 - Data Sovereignty, Privacy, Digital Identity & Trusted Territorial Data Exchange
    Manages purpose-based access control, privacy transformations, and cross-border sovereignty rules.
    """

    def evaluate_purpose_based_access(self, identity: Dict[str, Any], data_contract: Dict[str, Any], request_purpose: str) -> Dict[str, Any]:
        """
        B26.11 - Purpose-Based Access Control
        Ensures a user is not just authenticated, but has the right to use the data for a specific purpose.
        """
        allowed_purposes = data_contract.get("allowed_purposes", [])
        
        if request_purpose not in allowed_purposes:
            return {
                "decision": "DENY",
                "reason": f"Purpose '{request_purpose}' is not authorized by the data contract.",
                "audit_flag": "CONTRACT_VIOLATION_ATTEMPT"
            }
            
        return {
            "decision": "ALLOW",
            "reason": "Purpose authorized by contract.",
            "audit_flag": "NORMAL_ACCESS"
        }

    def enforce_sovereignty(self, data_asset: Dict[str, Any], consumer_jurisdiction: str) -> Dict[str, Any]:
        """
        B26.9 - Cross-Border Data Transfer Governance
        Prevents sensitive local data from leaving its designated sovereignty zone without policy approval.
        """
        asset_zone = data_asset.get("sovereignty_zone")
        classification = data_asset.get("classification")
        
        if classification == "SENSITIVE" and asset_zone != consumer_jurisdiction:
            return {
                "decision": "DENY",
                "reason": f"Sovereignty conflict: Cannot transfer SENSITIVE data from {asset_zone} to {consumer_jurisdiction}.",
                "federated_alternative_available": True
            }
            
        return {
            "decision": "ALLOW",
            "reason": "Sovereignty requirements met."
        }

    def trace_data_provenance(self, data_product_id: str, lineage_graph: Dict[str, Any]) -> List[str]:
        """
        B26.21 - Data Product Provenance
        Traces an intelligence product back to its raw data sources.
        """
        # Simplified recursive graph traversal mock
        lineage = []
        current_node = lineage_graph.get(data_product_id)
        
        while current_node:
            lineage.append(current_node.get("id"))
            current_node = lineage_graph.get(current_node.get("source_id"))
            
        return lineage
