import argparse
import time
import json
import random
from datetime import datetime, timezone

# We use the pipeline elements we've defined in previous sprints
from scripts.run_sprint_1 import MockYOLOTracker, MockLaneManager, MockSpeedEstimator, MockTrafficStateEngine

def run_pipeline(source: str):
    print(f"Initializing MoviSabio Intelligence Core v0.4 on source: {source}...\n")
    
    tracker = MockYOLOTracker()
    lane_manager = MockLaneManager()
    speed_estimator = MockSpeedEstimator()
    traffic_state = MockTrafficStateEngine()
    
    # Simulate processing video frames
    for frame_idx in range(1, 4):
        print(f"--- Processing Frame {frame_idx} ---")
        # Mock frame data
        frame = "mock_frame_data"
        
        # 1. Perception
        detections = tracker.process_frame(frame)
        vehicles_detected = len(detections)
        vehicles_tracked = vehicles_detected  # assuming no lost tracks for mock
        
        # 2. Lane Assignment
        detections = lane_manager.assign(detections)
        
        # 3. Speed & Queue Estimation
        detections = speed_estimator.estimate(detections)
        
        # 4. Traffic State Engine
        state = traffic_state.update("INT-001", detections)
        
        # Calculate totals
        lanes = state["lanes"]
        
        # Terminal Output Format specified in v0.4 milestone
        print(f"Vehicles detected: {vehicles_detected}")
        print(f"Vehicles tracked: {vehicles_tracked}\n")
        
        for lane_id, lane_data in lanes.items():
            print(f"Lane {lane_id}: {lane_data['vehicle_count']}")
            
        print(f"\nAverage speed: {round(sum([l['average_speed'] for l in lanes.values()]) / len(lanes), 1) if lanes else 0} km/h")
        print(f"Estimated queue: {sum([l['queue_length'] for l in lanes.values()])}")
        print(f"Congestion index: {round(random.uniform(0.4, 0.8), 2)}\n")
        
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MoviSabio v0.4 Traffic Intelligence Core")
    parser.add_argument("--source", type=str, required=True, help="Video source (e.g. traffic.mp4)")
    args = parser.parse_args()
    
    run_pipeline(args.source)
