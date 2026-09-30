import numpy as np

class KPIMetricsEngine:
    """
    Calculates and aggregates standard traffic engineering KPIs during simulation.
    """
    def __init__(self):
        self.step_metrics = []
        
    def record_step(self, traffic_state, current_signal):
        lanes = traffic_state.get("lanes", {})
        total_vehicles = sum(l.get("vehicle_count", 0) for l in lanes.values())
        total_queue = sum(l.get("queue_length", 0) for l in lanes.values())
        speeds = [l.get("average_speed", 0) for l in lanes.values() if l.get("vehicle_count", 0) > 0]
        avg_speed = np.mean(speeds) if speeds else 0
        
        self.step_metrics.append({
            "vehicles": total_vehicles,
            "queue": total_queue,
            "speed": avg_speed
        })
        
    def generate_report(self):
        if not self.step_metrics:
            return {}
            
        queues = [m["queue"] for m in self.step_metrics]
        speeds = [m["speed"] for m in self.step_metrics]
        
        return {
            "average_queue": float(np.mean(queues)),
            "max_queue": int(np.max(queues)),
            "average_speed_kmh": float(np.mean(speeds)),
            "95th_percentile_queue": float(np.percentile(queues, 95))
        }
