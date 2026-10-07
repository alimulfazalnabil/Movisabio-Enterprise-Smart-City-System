from typing import Dict, Any, List

class CircularIntelligenceEngine:
    """
    B17 - Smart Waste, Circular Economy, Materials & Resource Recovery Intelligence
    Models waste flows, route optimization, and industrial symbiosis.
    """

    def generate_dynamic_route(self, bins: List[Dict[str, Any]], vehicle_capacity: float) -> Dict[str, Any]:
        """
        B17.7 - Real-Time Waste Routing
        Selects bins that need collection and generates a route up to vehicle capacity.
        """
        # Filter bins requiring collection
        target_bins = [b for b in bins if b.get("current_fill_level_pct", 0) > 80.0]
        
        route = []
        current_load = 0.0
        
        for b in target_bins:
            if current_load + b.get("capacity_kg", 0) <= vehicle_capacity:
                route.append(b.get("bin_id"))
                current_load += b.get("capacity_kg", 0)
                
        return {
            "route_generated": True,
            "stops": route,
            "estimated_load_kg": current_load,
            "efficiency": "HIGH" if current_load > (vehicle_capacity * 0.8) else "LOW"
        }

    def match_industrial_symbiosis(self, supply: List[Dict[str, Any]], demand: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        B17.15 - Industrial Symbiosis Intelligence
        Matches waste byproducts from one entity with material demand from another.
        """
        matches = []
        for s in supply:
            for d in demand:
                if s.get("material_type") == d.get("material_type") and s.get("quantity_kg", 0) >= d.get("quantity_kg", 0):
                    matches.append({
                        "provider_id": s.get("provider_id"),
                        "receiver_id": d.get("receiver_id"),
                        "material": s.get("material_type"),
                        "fulfilled_kg": d.get("quantity_kg")
                    })
        return matches

    def forecast_facility_capacity(self, facility: Dict[str, Any], forecasted_waste: float) -> Dict[str, Any]:
        """
        B17.9 - Facility Capacity Forecasting
        Predicts when a waste facility will exceed processing capacity.
        """
        capacity = facility.get("processing_capacity_tpd", 100)
        current = facility.get("current_load_tpd", 50)
        
        future_load = current + forecasted_waste
        
        status = "HEALTHY"
        if future_load >= capacity:
            status = "CAPACITY_EXCEEDED"
        elif future_load >= (capacity * 0.9):
            status = "CRITICAL_WARNING"
            
        return {
            "facility_id": facility.get("facility_id", "UNKNOWN"),
            "projected_load_tpd": future_load,
            "capacity_status": status,
            "available_headroom_tpd": max(0, capacity - future_load)
        }
