import json
import datetime
from typing import List, Dict, Any

class MockYOLOTracker:
    def process_frame(self, frame: Any) -> List[Dict]:
        return [
            {"id": "v1", "class": "car", "bbox": [10, 10, 50, 50]},
            {"id": "v2", "class": "bus", "bbox": [100, 100, 200, 200]},
            {"id": "v3", "class": "car", "bbox": [30, 30, 70, 70]},
        ]

class MockLaneManager:
    def assign(self, detections: List[Dict]) -> List[Dict]:
        for idx, det in enumerate(detections):
            det["lane"] = "N1" if idx % 2 == 0 else "N2"
        return detections

class MockSpeedEstimator:
    def estimate(self, detections: List[Dict]) -> List[Dict]:
        for idx, det in enumerate(detections):
            det["speed"] = 31.4 if det["lane"] == "N1" else 25.7
        return detections

class MockTrafficStateEngine:
    def update(self, intersection_id: str, detections: List[Dict]) -> Dict:
        lanes = {}
        for det in detections:
            lane_id = det["lane"]
            if lane_id not in lanes:
                lanes[lane_id] = {"vehicle_count": 0, "total_speed": 0.0, "queue_length": 0}
            
            lanes[lane_id]["vehicle_count"] += 1
            lanes[lane_id]["total_speed"] += det["speed"]
            if det["speed"] < 10.0:
                lanes[lane_id]["queue_length"] += 1
                
        # Format for output
        formatted_lanes = {}
        for lane_id, data in lanes.items():
            avg_speed = data["total_speed"] / data["vehicle_count"] if data["vehicle_count"] > 0 else 0
            formatted_lanes[lane_id] = {
                "vehicle_count": data["vehicle_count"],
                "average_speed": round(avg_speed, 1),
                "queue_length": data["queue_length"]
            }

        return {
            "intersection_id": intersection_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "vehicles": len(detections),
            "lanes": formatted_lanes
        }

def run_sprint_1_pipeline():
    print("--- Running Sprint 1 Pipeline ---")
    
    # 1. Initialize modules
    tracker = MockYOLOTracker()
    lane_manager = MockLaneManager()
    speed_estimator = MockSpeedEstimator()
    traffic_state = MockTrafficStateEngine()
    
    # 2. Pipeline Execution
    frame = "mock_video_frame_bytes"
    
    detections = tracker.process_frame(frame)
    detections = lane_manager.assign(detections)
    detections = speed_estimator.estimate(detections)
    
    state_output = traffic_state.update("INT-001", detections)
    
    print(json.dumps(state_output, indent=2))

if __name__ == "__main__":
    run_sprint_1_pipeline()
