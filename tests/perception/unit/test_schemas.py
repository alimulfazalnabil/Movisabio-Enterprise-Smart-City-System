import pytest
from datetime import datetime, timezone
from src.services.perception.detection.models import Detection
from src.services.perception.tracking.lifecycle import VehicleTrack, BoundingBox
from src.services.perception.calibration.homography import CameraCalibration, Resolution, CalibrationPoint

def test_detection_schema():
    det = Detection(
        detection_id="det_01",
        camera_id="cam_01",
        frame_id="frame_01",
        class_id=0,
        class_name="car",
        confidence=0.98,
        bbox_x1=10, bbox_y1=10, bbox_x2=100, bbox_y2=100,
        timestamp=datetime.now(timezone.utc),
        model_name="yolov8",
        model_version="1.0"
    )
    assert det.class_name == "car"

def test_calibration_schema():
    calib = CameraCalibration(
        calibration_id="cal_01",
        camera_id="cam_01",
        version="v1",
        image_resolution=Resolution(width=1920, height=1080),
        reference_points=[
            CalibrationPoint(image=(0.0, 0.0), world=(0.0, 0.0))
        ],
        created_by="admin",
        created_at=datetime.now(timezone.utc),
        validated_at=datetime.now(timezone.utc),
        status="VALID"
    )
    assert calib.status == "VALID"
