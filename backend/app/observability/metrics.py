from typing import Dict

class MetricsRegistry:
    def __init__(self):
        self.counters: Dict[str, int] = {
            "frames_processed_total": 0,
            "detections_total": 0,
            "tracks_active": 0,
            "vehicles_counted_total": 0,
            "speed_estimation_errors": 0,
            "safety_rejections_total": 0,
            "signal_commands_total": 0,
            "signal_command_failures": 0,
            "corridor_commands_issued": 0
        }
        self.latencies: Dict[str, list] = {
            "traffic_state_latency": [],
            "optimization_latency": []
        }

    def inc(self, metric: str, amount: int = 1):
        if metric in self.counters:
            self.counters[metric] += amount

    def record_latency(self, metric: str, latency_ms: float):
        if metric in self.latencies:
            self.latencies[metric].append(latency_ms)

    def summary(self) -> dict:
        return {
            "counters": self.counters,
            "latencies": {k: (sum(v)/len(v) if v else 0) for k, v in self.latencies.items()}
        }

metrics = MetricsRegistry()
