from typing import Dict, Any, List

class SpatialIntelligenceEngine:
    """
    B15 - Territorial Land, Real Estate, Construction & Spatial Development Intelligence
    Assesses the territorial impact of proposed spatial development.
    """

    def analyze_spatial_constraints(self, proposal: Dict[str, Any], parcel: Dict[str, Any], zoning: Dict[str, Any]) -> Dict[str, Any]:
        """
        B15.6 - Spatial Constraint Engine
        Checks a proposal against zoning rules, physical constraints, and land use policies.
        """
        proposed_use = proposal.get("proposed_use", "")
        proposed_height = proposal.get("building_height_m", 0)
        
        hard_constraints = []
        soft_constraints = []
        
        # Check Zoning
        if proposed_use not in zoning.get("permitted_uses", []):
            hard_constraints.append(f"Proposed use '{proposed_use}' not permitted in zone.")
            
        max_height = zoning.get("max_height_m", 999)
        if proposed_height > max_height:
            hard_constraints.append(f"Proposed height {proposed_height}m exceeds zoning limit of {max_height}m.")
            
        # Check Physical constraints (mocked from parcel)
        if parcel.get("flood_zone") == "HIGH":
            soft_constraints.append("Parcel is in high flood risk zone. Mitigation required.")
            
        suitability = 100
        if hard_constraints:
            suitability = 0
        else:
            suitability -= len(soft_constraints) * 10
            
        return {
            "suitability_score": max(0, suitability),
            "hard_constraints": hard_constraints,
            "soft_constraints": soft_constraints,
            "viable": len(hard_constraints) == 0
        }

    def generate_traffic_impact(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        B15.14 - Traffic Generation Modeling
        Estimates the trip generation of a proposed development to interface with the B8 Mobility system.
        """
        # Very simplistic ITE-style trip generation mock
        pop = proposal.get("expected_population", 0)
        jobs = proposal.get("expected_jobs", 0)
        
        daily_trips = (pop * 2.5) + (jobs * 3.2)
        peak_hour_trips = daily_trips * 0.12
        
        return {
            "estimated_daily_trips": int(daily_trips),
            "estimated_peak_hour_trips": int(peak_hour_trips),
            "mobility_pressure": "HIGH" if peak_hour_trips > 500 else "MODERATE"
        }

    def evaluate_public_service_impact(self, proposal: Dict[str, Any], service_capacities: Dict[str, Any]) -> Dict[str, Any]:
        """
        B15.17 - Public-Service Capacity Impact
        Evaluates whether existing public services (schools, transit) can support the new population.
        """
        pop = proposal.get("expected_population", 0)
        
        school_capacity = service_capacities.get("school_seats_available", 0)
        expected_students = int(pop * 0.15) # Assume 15% school-aged
        
        school_impact = "Adequate"
        if expected_students > school_capacity:
            school_impact = f"Deficit: {expected_students - school_capacity} seats"
            
        return {
            "expected_new_students": expected_students,
            "school_capacity_impact": school_impact
        }
