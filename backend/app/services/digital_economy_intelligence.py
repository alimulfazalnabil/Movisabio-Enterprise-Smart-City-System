from typing import Dict, Any, List

class DigitalEconomyIntelligenceEngine:
    """
    B38 - Digital Economy, Technology Industry & Digital Transformation Intelligence
    Models digital maturity, workforce skill gaps, and digital transformation scenarios.
    """

    def calculate_digital_maturity(self, infrastructure_score: float, workforce_score: float, business_adoption: float, public_services: float) -> Dict[str, Any]:
        """
        B38.4 - Digital Maturity Engine
        Computes a composite digital maturity score.
        """
        # Weighted composite score
        overall = (infrastructure_score * 0.3) + (workforce_score * 0.3) + (business_adoption * 0.25) + (public_services * 0.15)
        
        # Determine level
        if overall >= 85:
            level = "Level 5 - Autonomous / Adaptive"
        elif overall >= 70:
            level = "Level 4 - Intelligent"
        elif overall >= 55:
            level = "Level 3 - Data-Driven"
        elif overall >= 35:
            level = "Level 2 - Connected"
        elif overall >= 15:
            level = "Level 1 - Digitized"
        else:
            level = "Level 0 - Offline"
            
        return {
            "overall_score": round(overall, 1),
            "maturity_level": level,
            "sub_scores": {
                "infrastructure": infrastructure_score,
                "workforce": workforce_score,
                "business": business_adoption,
                "public_services": public_services
            }
        }

    def analyze_skill_gap(self, skill_domain: str, current_supply: int, projected_demand: int) -> Dict[str, Any]:
        """
        B38.7 - Digital Skill Gap Intelligence
        Analyzes the gap between workforce supply and industry demand.
        """
        gap = current_supply - projected_demand
        gap_pct = (abs(gap) / projected_demand) * 100 if projected_demand > 0 else 0
        
        criticality = "HIGH" if gap < 0 and gap_pct > 20 else "MEDIUM" if gap < 0 else "LOW"
        
        return {
            "skill_domain": skill_domain,
            "gap_magnitude": gap,
            "gap_percentage": round(gap_pct, 1),
            "criticality": criticality,
            "status": "SHORTAGE" if gap < 0 else "SURPLUS"
        }

    def simulate_digital_investment(self, investment_amount_eur: float, sector: str, current_maturity: float) -> Dict[str, Any]:
        """
        B38.12 - Digital Transformation Scenario Engine
        Simulates the territorial impact of targeted digital investment.
        """
        # Simple multiplier logic based on current maturity (higher maturity = better absorption)
        absorption_factor = min(1.0, current_maturity / 100.0) + 0.2
        projected_economic_output = investment_amount_eur * absorption_factor * 1.5
        
        return {
            "investment_sector": sector,
            "investment_amount_eur": investment_amount_eur,
            "projected_economic_output": round(projected_economic_output, 2),
            "absorption_readiness": round(absorption_factor, 2),
            "note": "Output is highly dependent on parallel workforce skill development."
        }
