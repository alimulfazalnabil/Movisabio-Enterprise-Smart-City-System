from typing import List, Tuple
from src.services.water_waste.models.schemas import WasteBin, WasteBinState, WasteRouteRecommendation

class WasteRouteEngine:
    """
    Optimizes waste collection routes based on bin fill states and vehicle capacity.
    """
    
    def generate_route(self, vehicle_id: str, vehicle_capacity_kg: float, bins: List[WasteBin]) -> WasteRouteRecommendation:
        """
        Selects priority bins (High, Full, Overflow Risk) that fit within vehicle capacity.
        Note: This is a simplified bin-packing/filtering simulation. A true implementation 
        would use TSP/VRP routing algorithms.
        """
        priority_states = [WasteBinState.HIGH, WasteBinState.FULL, WasteBinState.OVERFLOW_RISK]
        
        # Filter for priority bins
        target_bins = [b for b in bins if b.state in priority_states]
        
        # Sort by urgency (Overflow > Full > High)
        state_weights = {WasteBinState.OVERFLOW_RISK: 3, WasteBinState.FULL: 2, WasteBinState.HIGH: 1}
        target_bins.sort(key=lambda b: state_weights.get(b.state, 0), reverse=True)
        
        selected_ids = []
        total_kg = 0.0
        
        for b in target_bins:
            # Estimate kg based on state and capacity
            est_fill = 0.8 # Assume 80% for HIGH
            if b.state == WasteBinState.FULL: est_fill = 1.0
            if b.state == WasteBinState.OVERFLOW_RISK: est_fill = 1.1
            
            bin_kg = b.capacity_kg * est_fill
            
            if total_kg + bin_kg <= vehicle_capacity_kg:
                selected_ids.append(b.bin_id)
                total_kg += bin_kg
                
        # Assume 10 mins per bin for routing demo
        return WasteRouteRecommendation(
            route_id=f"RT-{vehicle_id}",
            vehicle_id=vehicle_id,
            ordered_bin_ids=selected_ids,
            estimated_duration_min=len(selected_ids) * 10.0,
            total_expected_kg=total_kg
        )
