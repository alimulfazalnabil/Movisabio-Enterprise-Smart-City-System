from typing import Dict, Any, List

class IndustrialIntelligenceEngine:
    """
    B22 - Industrial, Manufacturing, Logistics & Supply-Chain Territorial Intelligence
    Analyzes supply-chain risk, factory bottlenecks, and predictive maintenance.
    """

    def simulate_supply_shock(self, supplier_id: str, duration_days: int, factories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B22.26 - Supply-Chain Shock Simulation
        Traces how a disruption at a single supplier propagates downstream.
        """
        affected_factories = []
        for factory in factories:
            if supplier_id in factory.get("critical_suppliers", []):
                inventory = factory.get("raw_material_buffer_days", 14)
                if duration_days > inventory:
                    affected_factories.append({
                        "factory_id": factory.get("factory_id"),
                        "days_until_shutdown": inventory
                    })
                    
        return {
            "disrupted_supplier": supplier_id,
            "shock_duration_days": duration_days,
            "systemic_risk_status": "CRITICAL" if len(affected_factories) > 0 else "MANAGEABLE",
            "factories_facing_shutdown": affected_factories
        }

    def detect_bottleneck(self, production_stages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        B22.6 - Manufacturing Bottleneck Intelligence
        Identifies the rate-limiting step in a production line.
        """
        if not production_stages:
            return {}
            
        # Find the stage with the lowest throughput capacity
        bottleneck = min(production_stages, key=lambda x: x.get("capacity_units_per_hour", 9999))
        max_capacity = max(production_stages, key=lambda x: x.get("capacity_units_per_hour", 0)).get("capacity_units_per_hour", 1)
        
        return {
            "bottleneck_stage": bottleneck.get("stage_name"),
            "current_throughput": bottleneck.get("capacity_units_per_hour"),
            "efficiency_loss_pct": round((1.0 - (bottleneck.get("capacity_units_per_hour") / max(1, max_capacity))) * 100, 1),
            "recommendation": f"Increase capacity at {bottleneck.get('stage_name')} to match line maximum."
        }

    def predict_machine_failure(self, machine_telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        B22.8 - Predictive Maintenance
        Evaluates machine sensor data to predict Remaining Useful Life (RUL).
        """
        vibration = machine_telemetry.get("vibration_hz", 50)
        temp = machine_telemetry.get("temp_c", 60)
        
        risk_score = 0
        if vibration > 120:
            risk_score += 50
        if temp > 85:
            risk_score += 30
            
        return {
            "machine_id": machine_telemetry.get("machine_id"),
            "anomaly_probability": round(risk_score / 100.0, 2),
            "estimated_rul_days": max(1, 30 - int(risk_score / 3)), # Mock RUL calculation
            "action_required": risk_score > 60
        }
