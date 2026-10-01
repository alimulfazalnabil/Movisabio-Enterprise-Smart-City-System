from pydantic import BaseModel
from datetime import datetime

class Detection(BaseModel):
    """
    Canonical Detection schema. Normalizes output from YOLO or other detectors.
    """
    detection_id: str
    camera_id: str
    frame_id: str
    class_id: int
    class_name: str
    confidence: float
    
    # Bounding Box coordinates
    bbox_x1: float
    bbox_y1: float
    bbox_x2: float
    bbox_y2: float
    
    timestamp: datetime
    model_name: str
    model_version: str
