import numpy as np
import cv2
from typing import List, Tuple
from backend.app.traffic.perception import Track

class SpeedEstimator:
    def __init__(self, calibration_matrix: List[List[float]]):
        """
        calibration_matrix: 3x3 homography matrix mapping image plane to ground plane
        """
        self.H = np.array(calibration_matrix) if calibration_matrix else np.eye(3)
        self.calibration_version = "v1"

    def image_to_world(self, pt: Tuple[float, float]) -> Tuple[float, float]:
        # Convert to homogeneous coords
        pt_h = np.array([pt[0], pt[1], 1.0])
        # Transform
        world_pt = self.H @ pt_h
        # Normalize
        world_pt = world_pt / world_pt[2]
        return (world_pt[0], world_pt[1])

    def estimate_speed(self, track: Track) -> float:
        if len(track.trajectory) < 2:
            return 0.0

        p1_img = track.trajectory[0]
        p2_img = track.trajectory[-1]
        
        t1 = track.first_seen.timestamp()
        t2 = track.last_seen.timestamp()
        
        dt = t2 - t1
        if dt <= 0:
            return 0.0

        p1_w = self.image_to_world(p1_img)
        p2_w = self.image_to_world(p2_img)

        # Distance in meters (assuming calibration maps to meters)
        dist = np.sqrt((p2_w[0] - p1_w[0])**2 + (p2_w[1] - p1_w[1])**2)
        
        speed_mps = dist / dt
        speed_kmh = speed_mps * 3.6
        return speed_kmh
