from typing import Dict, Any, List

class SocialIntelligenceEngine:
    """
    B36 - Social, Community, Equity & Quality-of-Life Intelligence
    Models territorial equity, service accessibility, and civic feedback.
    """

    def calculate_territorial_equity(self, service_access_score: float, environmental_burden_score: float, economic_opportunity_score: float) -> Dict[str, Any]:
        """
        B36.4 - Territorial Equity Model
        Computes a structural equity profile for a specific neighborhood or district.
        """
        # Normalize and invert environmental burden (higher burden = lower equity)
        inv_burden = 1.0 - environmental_burden_score
        
        # Simple composite (in reality, requires nuanced weighting)
        composite_score = (service_access_score + inv_burden + economic_opportunity_score) / 3.0
        
        return {
            "composite_equity_score": round(composite_score, 2),
            "service_accessibility": service_access_score,
            "environmental_burden": environmental_burden_score,
            "economic_opportunity": economic_opportunity_score,
            "status": "HIGH_DISPARITY" if composite_score < 0.4 else "EQUITABLE"
        }

    def evaluate_service_accessibility(self, population_density: int, distance_to_service_km: float, transit_availability_score: float) -> Dict[str, Any]:
        """
        B36.5 - Access-to-Service Intelligence
        Determines the effective accessibility of a critical service for a specific population group.
        """
        # Estimated travel time logic
        base_time_mins = distance_to_service_km * 12 # Assume 12 mins per km walking/slow transit
        adjusted_time = base_time_mins * (1.0 - (transit_availability_score * 0.5))
        
        return {
            "distance_km": distance_to_service_km,
            "estimated_transit_time_mins": round(adjusted_time, 1),
            "accessibility_rating": "POOR" if adjusted_time > 30 else "GOOD",
            "population_impacted": population_density
        }

    def aggregate_civic_feedback(self, feedback_reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B36.20 - Civic Feedback Intelligence
        Aggregates raw community reports to identify emerging structural issues.
        """
        issue_counts = {}
        for report in feedback_reports:
            topic = report.get("topic", "UNKNOWN")
            issue_counts[topic] = issue_counts.get(topic, 0) + 1
            
        if not issue_counts:
            return {"status": "NO_DATA"}
            
        top_issue = max(issue_counts, key=issue_counts.get)
        
        return {
            "total_reports": len(feedback_reports),
            "top_emerging_issue": top_issue,
            "issue_frequency": issue_counts[top_issue],
            "recommended_action": f"Trigger institutional review for {top_issue}"
        }
