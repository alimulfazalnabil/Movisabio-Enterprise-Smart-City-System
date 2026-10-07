from typing import Dict, Any, List

class InfrastructureIntelligenceEngine:
    """
    B11 - Territorial Infrastructure & Utility Intelligence
    Predicts failures, optimizes maintenance, and manages asset lifecycles.
    """

    def predict_remaining_useful_life(self, asset: Dict[str, Any], condition_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B11.8 - Remaining Useful Life (RUL) Prediction
        """
        age_years = asset.get("age_years", 0)
        expected_life = asset.get("expected_life_years", 20)
        
        # Simplistic survival model proxy
        base_rul = expected_life - age_years
        
        # Penalize RUL based on most recent condition
        if condition_history:
            latest_condition = condition_history[-1].get("state", "UNKNOWN")
            if latest_condition == "DEGRADED":
                base_rul *= 0.5
            elif latest_condition == "POOR":
                base_rul *= 0.2
            elif latest_condition == "CRITICAL":
                base_rul = 0.5 # 6 months
                
        # Confidence decays if condition history is missing or sparse
        confidence = 0.9 if len(condition_history) > 3 else 0.5
        
        return {
            "estimated_rul_years": max(0.0, base_rul),
            "confidence": confidence,
            "prediction_status": "PREDICTED"
        }

    def calculate_asset_risk(self, failure_probability: float, criticality_score: float) -> Dict[str, Any]:
        """
        B11.12 - Infrastructure Risk Model (Risk = Probability × Consequence)
        """
        risk_score = failure_probability * criticality_score
        
        if risk_score > 0.8:
            level = "CRITICAL"
        elif risk_score > 0.5:
            level = "HIGH"
        elif risk_score > 0.2:
            level = "MEDIUM"
        else:
            level = "LOW"
            
        return {
            "risk_score": risk_score,
            "risk_level": level,
            "mitigation_required": level in ["HIGH", "CRITICAL"]
        }

    def simulate_cascading_failure(self, root_asset_id: str, dependencies: Dict[str, List[str]]) -> List[str]:
        """
        B11.29 - Cascading Failure Simulation
        Given a root failure (e.g., Substation), recursively find all dependent assets.
        """
        failed_assets = set()
        queue = [root_asset_id]
        
        while queue:
            current = queue.pop(0)
            if current not in failed_assets:
                failed_assets.add(current)
                # Find assets that depend on `current`
                for asset, deps in dependencies.items():
                    if current in deps and asset not in failed_assets:
                        queue.append(asset)
                        
        return list(failed_assets)

    def optimize_maintenance_portfolio(self, assets: List[Dict[str, Any]], budget: float) -> List[Dict[str, Any]]:
        """
        B11.25 - Infrastructure Portfolio Optimization
        Greedy knapsack approximation for maintenance prioritization.
        """
        # Sort by highest risk/cost ratio
        sorted_assets = sorted(
            assets, 
            key=lambda x: (x.get("risk_score", 0) / max(x.get("repair_cost", 1), 0.1)), 
            reverse=True
        )
        
        selected = []
        spent = 0.0
        
        for asset in sorted_assets:
            cost = asset.get("repair_cost", 0)
            if spent + cost <= budget:
                selected.append(asset)
                spent += cost
                
        return selected
