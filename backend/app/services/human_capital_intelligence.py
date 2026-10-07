from typing import Dict, Any, List

class HumanCapitalIntelligenceEngine:
    """
    B20 - Education, Skills, Workforce & Human-Capital Territorial Intelligence
    Analyzes skills gaps, education capacity, and workforce accessibility.
    """

    def analyze_skills_gap(self, skill_demand: List[Dict[str, Any]], skill_supply: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        B20.8 - Skills Gap Intelligence
        Compares future job demand with current active workforce supply.
        """
        gaps = []
        for demand in skill_demand:
            skill = demand.get("skill")
            required = demand.get("count", 0)
            
            # Find matching supply
            available = sum(s.get("count", 0) for s in skill_supply if s.get("skill") == skill)
            
            gaps.append({
                "skill": skill,
                "demand": required,
                "supply": available,
                "gap": required - available
            })
            
        return gaps

    def evaluate_curriculum_alignment(self, course_skills: List[str], industry_demand: List[str]) -> Dict[str, Any]:
        """
        B20.12 - Curriculum Alignment Intelligence
        Advisory comparison of curriculum vs labor-market demand.
        """
        course_set = set(course_skills)
        demand_set = set(industry_demand)
        
        strong_alignment = course_set.intersection(demand_set)
        gaps = demand_set.difference(course_set)
        
        return {
            "alignment_score_pct": round(len(strong_alignment) / max(1, len(demand_set)) * 100, 1),
            "strong_coverage": list(strong_alignment),
            "identified_gaps": list(gaps),
            "advisory_note": "This is an advisory analysis based on aggregate industry postings, not an accreditation mandate."
        }

    def assess_jobs_housing_balance(self, zone_id: str, local_jobs: int, local_housing_units: int, transit_accessibility_score: float) -> Dict[str, Any]:
        """
        B20.14 - Jobs-Housing Balance
        Identifies areas where employment growth outstrips housing or transit.
        """
        ratio = local_jobs / max(1, local_housing_units)
        
        status = "BALANCED"
        if ratio > 1.5:
            status = "HOUSING_DEFICIT"
        elif ratio < 0.8:
            status = "EMPLOYMENT_DEFICIT"
            
        return {
            "zone_id": zone_id,
            "jobs_to_housing_ratio": round(ratio, 2),
            "status": status,
            "transit_mitigation": "STRONG" if transit_accessibility_score > 80 else "WEAK" if transit_accessibility_score < 40 else "MODERATE"
        }
