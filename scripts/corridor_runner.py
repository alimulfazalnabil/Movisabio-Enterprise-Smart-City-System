import time
from backend.app.traffic.corridor_optimizer import CorridorOptimizer
from backend.app.traffic.hierarchical_agent import CorridorAgent
from backend.app.observability.metrics import metrics

def run_corridor_simulation():
    print("Initializing B8 Multi-Intersection Corridor Intelligence Loop...")
    
    config = {"w_delay": 1.0, "w_spillback": 5.0}
    optimizer = CorridorOptimizer(config)
    
    intersections = ["INT-001", "INT-002", "INT-003"]
    agent = CorridorAgent("CORRIDOR-A", intersections)
    
    # Mock Graph
    network_graph = {
        "nodes": intersections,
        "edges": {
            "INT-001": ["INT-002"],
            "INT-002": ["INT-003"],
            "INT-003": []
        }
    }
    
    for step in range(5):
        print(f"\n--- Network Step {step} ---")
        
        # 1. Gather Corridor State
        mock_states = {
            "INT-001": {"queue_length": 50, "arrival_flow": 1200, "departure_flow": 1000},
            "INT-002": {"queue_length": 180, "capacity": 200, "arrival_flow": 1000, "departure_flow": 400}, # Bottleneck
            "INT-003": {"queue_length": 10, "capacity": 200, "arrival_flow": 400, "departure_flow": 800}
        }
        
        # 2. Corridor Optimizer computes Spillback & Bottlenecks
        proposals = optimizer.optimize_corridor("CORRIDOR-A", network_graph, mock_states)
        for idx, prop in proposals.items():
            print(f"[{idx}] Optimizer Proposal: {prop['action']} | {prop['explanation']}")
            
        # 3. Hierarchical Control
        corridor_context = {"spillback_risks": {"INT-001": 0.9, "INT-002": 0.1}}
        hierarchical_commands = agent.coordinate(corridor_context)
        
        for idx, cmd in hierarchical_commands.items():
            print(f"[{idx}] Hierarchical Agent Issued: {cmd['requested_phase']} for {cmd.get('duration')}s")
            metrics.inc("corridor_commands_issued")
            
        time.sleep(1)

if __name__ == "__main__":
    run_corridor_simulation()
