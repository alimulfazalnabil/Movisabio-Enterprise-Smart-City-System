from typing import Dict, Any, List

class SecurityIntelligenceEngine:
    """
    B25 - Cybersecurity, Cyber-Physical Security & Digital Trust
    Calculates vulnerability priorities, correlates threats, and maps cyber-physical impacts.
    """

    def prioritize_vulnerability(self, cvss_score: float, criticality_level: str) -> Dict[str, Any]:
        """
        B25.12 - Risk-Based Vulnerability Prioritization
        Adjusts raw CVSS score based on the specific territorial criticality of the asset.
        """
        crit_multiplier = {
            "C0": 0.1, 
            "C1": 0.5, 
            "C2": 1.0, 
            "C3": 2.0, 
            "C4": 5.0, 
            "C5": 10.0
        }.get(criticality_level, 1.0)
        
        territorial_risk_score = cvss_score * crit_multiplier
        
        priority = "LOW"
        if territorial_risk_score > 50:
            priority = "CRITICAL"
        elif territorial_risk_score > 20:
            priority = "HIGH"
        elif territorial_risk_score > 10:
            priority = "MEDIUM"
            
        return {
            "territorial_risk_score": territorial_risk_score,
            "priority_level": priority
        }

    def correlate_threats(self, security_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B25.18 - Threat Correlation
        Looks for patterns like credential anomalies + unusual network traffic.
        """
        if not security_events:
            return {"status": "NO_EVENTS"}
            
        event_types = set([e.get("event_type") for e in security_events])
        
        if "FAILED_LOGIN" in event_types and "FIRMWARE_ANOMALY" in event_types:
            return {
                "status": "CRITICAL_SITUATION",
                "hypothesis": "Possible IoT device compromise and firmware tampering.",
                "recommended_action": "Isolate device network immediately."
            }
            
        return {
            "status": "NORMAL",
            "hypothesis": "Isolated events.",
            "recommended_action": "Monitor."
        }

    def evaluate_cyber_physical_dependency(self, compromised_asset_id: str, dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        B25.21 - Cyber-Physical Dependency Graph
        Maps a cyber event down to its physical/territorial consequences.
        """
        downstream_impacts = dependency_graph.get(compromised_asset_id, [])
        
        safety_critical = any(["Traffic" in impact or "Hospital" in impact for impact in downstream_impacts])
        
        return {
            "compromised_asset": compromised_asset_id,
            "physical_systems_at_risk": downstream_impacts,
            "safety_critical_impact": safety_critical,
            "response_posture": "S3 (Human-approved response)" if safety_critical else "S4 (Policy-authorized response)"
        }
