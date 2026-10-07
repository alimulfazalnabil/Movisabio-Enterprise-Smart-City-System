from typing import Dict, Any, List

class FinancialIntelligenceEngine:
    """
    B27 - Financial, Economic, Commerce, Payments & Territorial Financial Intelligence
    Evaluates infrastructure investments, stress tests economic shocks, and models trade dependencies.
    """

    def optimize_investment_portfolio(self, available_budget: float, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B27.15 - Public Investment Optimization
        Selects a portfolio of projects maximizing public/economic value under a budget constraint.
        (Simplified greedy knapsack approximation for demonstration)
        """
        # Sort by value/cost ratio
        for p in projects:
            p['roi'] = (p.get('expected_economic_value', 0) + p.get('expected_public_value', 0)) / max(1, p.get('capital_cost', 1))
            
        sorted_projects = sorted(projects, key=lambda x: x['roi'], reverse=True)
        
        selected = []
        spent = 0.0
        total_economic = 0.0
        
        for p in sorted_projects:
            if spent + p.get('capital_cost', 0) <= available_budget:
                selected.append(p.get('name'))
                spent += p.get('capital_cost', 0)
                total_economic += p.get('expected_economic_value', 0)
                
        return {
            "allocated_budget": spent,
            "remaining_budget": available_budget - spent,
            "selected_projects": selected,
            "projected_economic_value": total_economic
        }

    def simulate_economic_shock(self, territory_profile: Dict[str, Any], shock_type: str) -> Dict[str, Any]:
        """
        B27.30 - Financial Stress Testing
        Models cascading impacts of interest rate hikes or energy shocks.
        """
        if shock_type == "INTEREST_RATE_HIKE":
            return {
                "shock_scenario": "Interest Rate +200bps",
                "construction_activity_impact": "-15%",
                "sme_financing_gap": "+$45M",
                "recommended_intervention": "Deploy targeted municipal credit guarantees for critical infrastructure contractors."
            }
        
        if shock_type == "ENERGY_SHOCK":
            return {
                "shock_scenario": "Energy Price +40%",
                "industrial_margin_impact": "-8.5%",
                "retail_spending_impact": "-3.2%",
                "recommended_intervention": "Accelerate grid efficiency retrofits (B23)."
            }
            
        return {"status": "UNKNOWN_SHOCK"}

    def map_trade_dependency(self, commodity: str, local_demand_tons: float) -> Dict[str, Any]:
        """
        B27.22 - Trade Dependency Graph
        Evaluates the economic impact of a specific commodity disruption.
        """
        critical_sectors = ["Construction", "Manufacturing"] if commodity in ["Steel", "Aluminum"] else ["Agriculture", "Retail"]
        
        return {
            "disrupted_commodity": commodity,
            "dependent_sectors": critical_sectors,
            "estimated_local_shortage_tons": local_demand_tons * 0.4,
            "economic_risk": "HIGH",
            "mitigation_strategy": "Activate secondary suppliers in neighboring Sovereignty Zone."
        }
