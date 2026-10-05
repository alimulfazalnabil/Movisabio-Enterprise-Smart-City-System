from src.services.energy.models.schemas import GridCongestionState

class GridCongestionEngine:
    def evaluate_congestion(self, asset_id: str, territory_id: str, load_kw: float, capacity_kw: float) -> GridCongestionState:
        """
        Evaluates the congestion state of a grid asset (e.g. transformer or feeder).
        """
        if capacity_kw <= 0:
            ratio = 0.0
        else:
            ratio = load_kw / capacity_kw
            
        state = "NORMAL"
        if ratio >= 1.05:
            state = "FAILURE_RISK"
        elif ratio >= 0.95:
            state = "CONGESTED"
        elif ratio >= 0.85:
            state = "CONSTRAINED"
        elif ratio >= 0.75:
            state = "ELEVATED"
            
        return GridCongestionState(
            asset_id=asset_id,
            territory_id=territory_id,
            current_load_kw=load_kw,
            rated_capacity_kw=capacity_kw,
            state=state,
            confidence=0.9,
            time_horizon_minutes=0
        )
