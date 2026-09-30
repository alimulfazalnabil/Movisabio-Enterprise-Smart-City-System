import time
from src.perception.video.camera_health import CameraHealthMonitor
from src.perception.tracking.tracker import ObjectTracker
from src.perception.telemetry_agent import EdgeTelemetryAgent

class EdgePerceptionPipeline:
    """
    The orchestrator that runs on the Municipal Edge Node.
    Reads frames, runs YOLO/Tracker, calculates lanes/speeds, and publishes telemetry.
    """
    def __init__(self, camera_id: str):
        self.camera_id = camera_id
        self.health_monitor = CameraHealthMonitor(camera_id)
        self.tracker = ObjectTracker()
        self.telemetry = EdgeTelemetryAgent(f"EDGE-{camera_id}")
        
    def process_frame(self, frame_data):
        start_time = time.time()
        
        # 1. YOLO Detection (Mocked)
        raw_detections = [{"class": "car", "confidence": 0.95}] * 12
        
        # 2. Tracking
        tracked_objects = self.tracker.update(raw_detections)
        
        # 3. Lane Association & Speed (Mocked aggregation)
        traffic_state = {
            "timestamp": time.time(),
            "lanes": {
                "N1": {"vehicle_count": len(tracked_objects), "average_speed": 35.2, "queue_length": 2, "confidence": 0.93}
            }
        }
        
        # 4. Record Health
        inference_time = (time.time() - start_time) * 1000 # ms
        self.health_monitor.record_frame(inference_time)
        
        # 5. Publish Telemetry
        self.telemetry.publish("traffic_state_update", traffic_state)
        self.telemetry.publish("camera_health", self.health_monitor.check_health())
        
        return traffic_state
