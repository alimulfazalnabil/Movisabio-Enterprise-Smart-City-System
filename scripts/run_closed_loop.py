import time
import json
from scripts.run_sprint_1 import MockTrafficStateEngine
from services.optimization.rule_based_optimizer import RuleBasedOptimizer
from services.traffic_controller.mock_controller import TrafficSignalController

class MockTraCI:
    """Simulates SUMO TraCI API sending detection data and receiving light phases."""
    def __init__(self):
        self.step = 0
        # Initially, E/W is heavily congested, N/S is empty
        
    def simulation_step(self):
        self.step += 1
        # Generate mock detections based on step
        if self.step < 3:
            # E/W getting backed up
            return [
                {"id": f"v{i}", "class": "car", "lane": "E1", "speed": 0.0} for i in range(15)
            ] + [{"id": f"v{i}", "class": "car", "lane": "N1", "speed": 40.0} for i in range(2)]
        else:
            # E/W cleared out, N/S getting backed up
            return [
                {"id": f"v{i}", "class": "car", "lane": "N1", "speed": 0.0} for i in range(12)
            ] + [{"id": f"v{i}", "class": "car", "lane": "E1", "speed": 40.0} for i in range(1)]
            
    def set_phase(self, phase: str):
        print(f"[TraCI] SUMO Traffic Light set to: {phase}")

def run_closed_loop():
    print("--- Running SUMO Closed-Loop Digital Twin Simulation ---\n")
    
    traci = MockTraCI()
    state_engine = MockTrafficStateEngine()
    optimizer = RuleBasedOptimizer()
    controller = TrafficSignalController("configs/int_001.json")
    
    for i in range(5):
        print(f"\n=== SIMULATION TICK {i+1} ===")
        
        # 1. SUMO generates traffic -> Perception detects
        raw_detections = traci.simulation_step()
        
        # 2. Traffic State Engine builds macroscopic state
        traffic_state = state_engine.update("INT-001", raw_detections)
        print(f"Traffic State -> N1 Queue: {traffic_state['lanes'].get('N1', {}).get('queue_length', 0)} | E1 Queue: {traffic_state['lanes'].get('E1', {}).get('queue_length', 0)}")
        
        # 3. Optimizer evaluates state vs current signal
        current_signal = controller.get_state()
        decision = optimizer.evaluate(traffic_state, current_signal)
        print(f"Optimizer proposes: {decision['requested_action']} to {decision['requested_phase']} (Reason: {decision['reason']})")
        
        # 4. Safety & Controller process request
        if decision['requested_action'] != "MAINTAIN":
            audit = controller.request_action(
                requested_action=decision['requested_action'],
                requested_phase=decision['requested_phase'],
                reason=decision['reason'],
                optimizer=decision['optimizer']
            )
            print(f"Controller Status: {audit['controller_status']} (Safety: {audit['safety_status']})")
            
            # 5. Send safe command back to SUMO
            if audit['controller_status'] == "ACKNOWLEDGED":
                traci.set_phase(audit['requested_phase'])
        else:
            print("Controller Status: NO_CHANGE")
            
        time.sleep(1)

if __name__ == "__main__":
    run_closed_loop()
