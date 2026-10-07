from typing import Dict, Any, List

class InternationalIntelligenceEngine:
    """
    B31 - International, Cross-Border & Multi-Jurisdictional Territorial Intelligence
    Manages federation data exchange policies, cross-border bottlenecks, and shared environmental systems.
    """

    def validate_federated_exchange(self, source_policy: Dict[str, Any], requested_classification: str, requested_purpose: str) -> bool:
        """
        B31.3 - Cross-Border Data Exchange
        Validates whether a cross-border data request complies with the source territory's sovereignty policy.
        """
        allowed_classifications = source_policy.get("allowed_export_classifications", ["PUBLIC"])
        allowed_purposes = source_policy.get("allowed_export_purposes", ["RESEARCH"])
        
        if requested_classification not in allowed_classifications:
            return False
            
        if requested_purpose not in allowed_purposes:
            return False
            
        return True

    def simulate_cross_border_bottleneck(self, gateway_capacity: int, projected_freight_volume: int) -> Dict[str, Any]:
        """
        B31.5 - International Traffic Intelligence
        Models delays and economic impact of cross-border congestion.
        """
        if projected_freight_volume > gateway_capacity:
            excess = projected_freight_volume - gateway_capacity
            delay_hours = (excess / gateway_capacity) * 24
            
            return {
                "gateway_status": "CONGESTED",
                "excess_volume": excess,
                "projected_delay_hours": round(delay_hours, 1),
                "supply_chain_risk": "HIGH" if delay_hours > 12 else "MODERATE"
            }
            
        return {
            "gateway_status": "NORMAL",
            "projected_delay_hours": 0.0,
            "supply_chain_risk": "LOW"
        }

    def map_shared_infrastructure_dependency(self, asset_type: str, connected_territories: List[str]) -> Dict[str, Any]:
        """
        B31.7 - Cross-Border Infrastructure Dependencies
        Evaluates the geopolitical/resilience risk of shared infrastructure.
        """
        criticality = "HIGH" if len(connected_territories) > 2 or asset_type in ["POWER_GRID", "PIPELINE"] else "MEDIUM"
        
        return {
            "asset_type": asset_type,
            "connected_territories": connected_territories,
            "dependency_level": criticality,
            "federation_coordination_required": True if criticality == "HIGH" else False
        }
