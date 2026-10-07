from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter()

# B25.40 - Security APIs
@router.post("/vulnerabilities/prioritize", response_model=Dict[str, Any])
def prioritize_vulnerability(vuln: Dict[str, Any]):
    """B25.12 - Risk-Based Vulnerability Prioritization"""
    cvss = vuln.get("cvss_score", 5.0)
    criticality = vuln.get("asset_criticality", "C2")
    
    crit_multiplier = {"C0": 0.1, "C1": 0.5, "C2": 1.0, "C3": 2.0, "C4": 5.0, "C5": 10.0}.get(criticality, 1.0)
    risk_score = cvss * crit_multiplier
    
    priority = "LOW"
    if risk_score > 50:
        priority = "CRITICAL"
    elif risk_score > 20:
        priority = "HIGH"
    elif risk_score > 10:
        priority = "MEDIUM"
        
    return {
        "vulnerability_id": vuln.get("vuln_id", "VULN-001"),
        "raw_cvss": cvss,
        "territorial_risk_score": round(risk_score, 1),
        "priority_level": priority,
        "recommendation": "Immediate patch required." if priority == "CRITICAL" else "Schedule patch."
    }

@router.post("/incidents/correlate", response_model=Dict[str, Any])
def correlate_security_events(events: List[Dict[str, Any]]):
    """B25.18 - Threat Correlation"""
    if len(events) >= 3:
        return {
            "status": "SITUATION_DETECTED",
            "correlated_events": len(events),
            "hypothesis": "Coordinated identity compromise and unusual network activity.",
            "severity": "HIGH",
            "recommended_action": "Isolate affected identity and step-up authentication."
        }
    return {
        "status": "NORMAL",
        "correlated_events": len(events),
        "hypothesis": "Isolated events.",
        "severity": "LOW"
    }

@router.post("/scenarios/cyber-physical", response_model=Dict[str, Any])
def simulate_cyber_physical_impact(scenario: Dict[str, Any]):
    """B25.32 - Security Risk Digital Twin"""
    compromised_asset = scenario.get("compromised_asset", "Edge Gateway A")
    
    return {
        "scenario": f"Compromise of {compromised_asset}",
        "downstream_physical_impacts": [
            "Traffic Controller 12 (Loss of coordination)",
            "Intersection 5 Camera (Loss of feed)"
        ],
        "safety_risk_level": "HIGH",
        "authorized_response": "Sever Edge Gateway connection; activate local fallback mode for Traffic Controller 12."
    }
