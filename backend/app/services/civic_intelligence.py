from typing import Dict, Any, List
from datetime import datetime, timezone

class CivicIntelligenceEngine:
    """
    B13 - Smart Public Services, Government & Citizen Intelligence
    Provides case routing, SLA tracking, and civic demand intelligence.
    """

    def route_service_request(self, request_description: str, location: Dict[str, Any]) -> Dict[str, str]:
        """
        B13.12 - Intelligent Case Routing
        Classifies request and routes to appropriate government agency/team.
        """
        desc = request_description.lower()
        if "pothole" in desc or "road" in desc:
            return {"agency": "Department of Transportation", "team": "Road Maintenance", "priority": "MEDIUM"}
        elif "trash" in desc or "waste" in desc or "garbage" in desc:
            return {"agency": "Sanitation Department", "team": "Waste Collection", "priority": "LOW"}
        elif "light" in desc or "signal" in desc:
            return {"agency": "Department of Transportation", "team": "Traffic Signals", "priority": "HIGH"}
        elif "water" in desc or "leak" in desc:
            return {"agency": "Water Authority", "team": "Emergency Repair", "priority": "CRITICAL"}
        
        return {"agency": "General Services", "team": "Triage", "priority": "LOW"}

    def predict_sla_breach(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        B13.13 - SLA Intelligence
        Predicts whether an open case is likely to breach its Service Level Agreement.
        """
        deadline = request.get("sla_deadline")
        if not deadline:
            return {"risk": "UNKNOWN", "escalation_recommended": False}
            
        # Simplified logic: if less than 20% of the SLA time window remains and status is still in early phases
        now = datetime.now(timezone.utc)
        created_at = request.get("created_at", now)
        
        total_allowed = (deadline - created_at).total_seconds()
        elapsed = (now - created_at).total_seconds()
        
        status = request.get("status", "SUBMITTED")
        
        if total_allowed > 0:
            progress_pct = elapsed / total_allowed
            
            if progress_pct > 0.8 and status in ["SUBMITTED", "VALIDATING", "ASSIGNED"]:
                return {"risk": "HIGH", "escalation_recommended": True, "reason": "SLA deadline approaching and work not started."}
        
        return {"risk": "LOW", "escalation_recommended": False, "reason": "SLA on track."}

    def aggregate_civic_demand(self, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B13.16 - Civic Demand Intelligence
        Identifies geographic hotspots to transition from reactive to systemic repair.
        """
        # Very simple aggregation by district or mock location
        hotspots = {}
        for req in requests:
            loc = req.get("district", "Unknown")
            issue_type = req.get("issue_type", "General")
            
            if loc not in hotspots:
                hotspots[loc] = {}
            if issue_type not in hotspots[loc]:
                hotspots[loc][issue_type] = 0
            hotspots[loc][issue_type] += 1
            
        return {"hotspots_identified": hotspots}

    def check_human_ai_governance_boundary(self, action: str, classification: str) -> bool:
        """
        B13.33 - Human-AI Governance Boundary
        Ensures AI does not autonomously execute high-impact decisions regarding citizens.
        """
        restricted_actions = ["DENY_BENEFIT", "ISSUE_PENALTY", "REVOKE_PERMIT", "APPROVE_IDENTITY"]
        if action in restricted_actions:
            return False # Must go to Human / Authorized Workflow
            
        return True # AI can proceed (e.g. Draft response, Route case)
