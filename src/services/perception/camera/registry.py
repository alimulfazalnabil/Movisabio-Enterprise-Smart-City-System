from pydantic import BaseModel, Field
from typing import Optional

class CameraSource(BaseModel):
    type: str = "rtsp"
    uri_ref: str  # Secret reference, not the actual plaintext credentials
    protocol: str = "rtsp"

class CameraConfig(BaseModel):
    resolution: str
    target_fps: int
    inference_fps: int

class ModelConfig(BaseModel):
    name: str
    version: str
    device: str

class CameraStatus(BaseModel):
    enabled: bool
    processing_mode: str  # edge or cloud

class RegisteredCamera(BaseModel):
    camera_id: str
    tenant_id: str
    site_id: str
    intersection_id: str
    
    source: CameraSource
    configuration: CameraConfig
    model: ModelConfig
    calibration_profile_id: str
    status: CameraStatus
