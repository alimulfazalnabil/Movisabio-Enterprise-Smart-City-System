from typing import Dict, Any, List

class ResourceIntelligenceEngine:
    """
    B16 - Smart Energy, Utilities, Grid & Territorial Resource Intelligence
    Models resource flows, EV charging optimization, and cascading infrastructure failures.
    """

    def optimize_ev_charging(self, charging_demand: float, grid_capacity: float, renewable_forecast: float) -> Dict[str, Any]:
        """
        B16.11 - Smart EV Charging
        Optimizes charging power to stay within grid limits and maximize renewable use.
        """
        # Simplistic optimization logic
        max_allowable_draw = grid_capacity * 0.9 # Keep 10% safety margin
        
        # If demand exceeds allowable draw, we must curtail
        curtailment_needed = False
        allocated_power = charging_demand
        
        if charging_demand > max_allowable_draw:
            allocated_power = max_allowable_draw
            curtailment_needed = True
            
        # Calculate renewable mix
        renewable_pct = min(1.0, renewable_forecast / max(allocated_power, 1.0))
        
        return {
            "requested_kw": charging_demand,
            "allocated_kw": allocated_power,
            "curtailment_active": curtailment_needed,
            "renewable_mix_pct": round(renewable_pct * 100, 1),
            "recommendation": "SMART_CURTAILMENT" if curtailment_needed else "FULL_CHARGE"
        }

    def detect_water_leak(self, expected_flow: float, observed_flow: float, pressure_drop: float) -> Dict[str, Any]:
        """
        B16.14 - Water Leak Intelligence
        Detects likely water leaks by comparing expected vs observed flow and pressure anomalies.
        """
        flow_variance = observed_flow - expected_flow
        
        if flow_variance > (expected_flow * 0.15) and pressure_drop > 10.0:
            return {
                "leak_probability": 0.87,
                "confidence": "HIGH",
                "evidence": ["High flow variance", "Significant pressure drop"],
                "status": "ANOMALY_DETECTED"
            }
        elif flow_variance > (expected_flow * 0.05):
            return {
                "leak_probability": 0.40,
                "confidence": "LOW",
                "evidence": ["Minor flow variance"],
                "status": "MONITORING"
            }
            
        return {"leak_probability": 0.0, "status": "NORMAL"}

    def model_cascading_outage(self, source_failure: Dict[str, Any], dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        B16.19 - Cascading Utility Failure Intelligence
        Traces how a failure in one utility (e.g. Power) affects downstream systems (Water, Traffic).
        """
        failed_node = source_failure.get("node_id", "UNKNOWN")
        
        cascading_impacts = []
        if failed_node in dependency_graph:
            for dependent_asset in dependency_graph[failed_node]:
                cascading_impacts.append(dependent_asset)
                
        return {
            "source_failure": failed_node,
            "direct_cascading_failures_predicted": cascading_impacts,
            "severity_escalation": "HIGH" if len(cascading_impacts) > 2 else "MODERATE"
        }
