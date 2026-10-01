from typing import List, Tuple
from pydantic import BaseModel
from datetime import datetime

class CalibrationPoint(BaseModel):
    image: Tuple[float, float]
    world: Tuple[float, float]

class Resolution(BaseModel):
    width: int
    height: int

class CameraCalibration(BaseModel):
    """
    Homography/Perspective Transformation Profile mapping pixels to physical meters.
    """
    calibration_id: str
    camera_id: str
    version: str
    
    image_resolution: Resolution
    reference_points: List[CalibrationPoint]
    
    created_by: str
    created_at: datetime
    validated_at: datetime
    status: str  # VALID, INVALID

    def image_to_world(self, x: float, y: float) -> Tuple[float, float]:
        """
        Stub for CV2 Homography warpPerspective.
        Converts pixel coordinates to physical world coordinates (e.g. meters).
        """
        # OpenCV logic will be implemented here
        return (0.0, 0.0)
