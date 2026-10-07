from typing import Dict, Any, List

class ScienceInnovationIntelligenceEngine:
    """
    B37 - Science, Research, Innovation & Knowledge-Economy Intelligence
    Models research ecosystems, innovation clusters, and technology commercialization.
    """

    def analyze_innovation_cluster(self, domain: str, research_strength: float, venture_capital_available: float, talent_availability: float) -> Dict[str, Any]:
        """
        B37.18 - Innovation Cluster Intelligence
        Evaluates the maturity and bottlenecks of a specific technology cluster (e.g., AI or Biotech).
        """
        # Simple heuristic model for cluster maturity
        score = (research_strength * 0.4) + (venture_capital_available * 0.4) + (talent_availability * 0.2)
        
        if score > 0.8:
            maturity = "MATURE"
        elif score > 0.5:
            maturity = "GROWING"
        else:
            maturity = "EMERGING"
            
        bottleneck = "TALENT" if talent_availability < min(research_strength, venture_capital_available) else "FUNDING"
        
        return {
            "domain": domain,
            "maturity_stage": maturity,
            "cluster_score": round(score, 2),
            "primary_bottleneck": bottleneck
        }

    def evaluate_technology_transfer(self, current_trl: int, patents_filed: int, industry_partners: int) -> Dict[str, Any]:
        """
        B37.17 - University-Industry Intelligence
        Assesses the commercialization readiness of academic research.
        """
        readiness_score = current_trl + (patents_filed * 0.5) + (industry_partners * 1.5)
        
        return {
            "current_trl": current_trl,
            "commercialization_readiness_score": round(readiness_score, 1),
            "status": "READY_FOR_PILOT" if current_trl >= 6 and industry_partners > 0 else "EARLY_RESEARCH",
            "recommended_action": "Seek industry pilot partner" if industry_partners == 0 and current_trl > 4 else "Continue lab validation"
        }

    def simulate_innovation_policy(self, funding_increase_pct: float, current_researcher_count: int, current_startup_rate: float) -> Dict[str, Any]:
        """
        B37.26 - Innovation Policy Simulation
        Simulates the downstream territorial economic impact of increased R&D funding.
        """
        projected_researchers = current_researcher_count * (1 + (funding_increase_pct / 100))
        projected_startups = current_startup_rate * (1 + (funding_increase_pct / 100) * 1.5) # Assuming leverage effect
        
        return {
            "policy_input": f"+{funding_increase_pct}% R&D Funding",
            "projected_researchers": int(projected_researchers),
            "projected_annual_startups": round(projected_startups, 1),
            "economic_multiplier_est": 2.4, # Rule of thumb multiplier
            "time_to_impact": "3 to 5 years"
        }
