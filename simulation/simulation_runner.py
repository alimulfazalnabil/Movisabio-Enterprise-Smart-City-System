import time
import json
import os
from simulation.traci_client import TraCIClient
from simulation.metrics import KPIMetricsEngine
from services.traffic_controller.sumo_controller import SumoController
from services.optimization.rule_based_optimizer import RuleBasedOptimizer
from services.prediction.predictor import TrafficPredictor
from scripts.run_sprint_1 import MockTrafficStateEngine

def run_simulation(scenario_name: str, use_movisabio: bool):
    print(f"\n--- Starting SUMO Simulation: {scenario_name} ---")
    print(f"Controller: {'MoviSabio AI' if use_movisabio else 'Fixed-Time Baseline'}")
    
    traci = TraCIClient()
    traci.connect(["sumo", "-c", f"simulation/sumo/scenarios/{scenario_name}.sumocfg"])
    
    controller = SumoController("configs/int_001.json", traci_client=traci)
    optimizer = RuleBasedOptimizer()
    predictor = TrafficPredictor(active_model="gru")
    state_engine = MockTrafficStateEngine()
    metrics = KPIMetricsEngine()
    
    # 50 step simulation loop
    for step in range(1, 51):
        # 1. SUMO Environment state
        raw_detections = traci.get_vehicle_state("INT-001")
        
        # 2. MoviSabio Perception (Traffic State)
        traffic_state = state_engine.update("INT-001", raw_detections)
        
        # 3. Predict Future Traffic
        forecast = predictor.update_and_predict(traffic_state)
        
        # 4. AI Optimizer & Safety (only if using MoviSabio)
        if use_movisabio:
            current_signal = controller.get_state()
            # Optimizer now considers forecast as well
            decision = optimizer.evaluate(traffic_state, current_signal, forecast=forecast)
            
            if decision['requested_action'] != "MAINTAIN":
                controller.request_action(
                    requested_action=decision['requested_action'],
                    requested_phase=decision['requested_phase'],
                    reason=decision['reason'],
                    optimizer=decision['optimizer']
                )
                
        # 4. Advance Simulation and Record
        traci.advance()
        metrics.record_step(traffic_state, controller.get_state())
        
    traci.close()
    
    report = metrics.generate_report()
    print("Simulation Complete. KPIs:")
    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    run_simulation("evening_peak", use_movisabio=True)
