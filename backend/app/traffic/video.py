from abc import ABC, abstractmethod
from typing import Optional, Any
import numpy as np

class Frame:
    def __init__(self, frame_id: int, image: np.ndarray, timestamp: float):
        self.frame_id = frame_id
        self.image = image
        self.timestamp = timestamp

class VideoSource(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass
        
    @abstractmethod
    def get_frame(self) -> Optional[Frame]:
        pass
        
    @abstractmethod
    def disconnect(self):
        pass

class RTSPSource(VideoSource):
    def __init__(self, url: str):
        self.url = url
        self._connected = False
        self._frame_count = 0
        
    def connect(self) -> bool:
        self._connected = True
        return True
        
    def get_frame(self) -> Optional[Frame]:
        if not self._connected:
            return None
        self._frame_count += 1
        # Mock empty frame
        return Frame(self._frame_count, np.zeros((1080, 1920, 3)), 0.0)
        
    def disconnect(self):
        self._connected = False

class FileSource(VideoSource):
    def __init__(self, path: str):
        self.path = path
        
    def connect(self) -> bool:
        return True
        
    def get_frame(self) -> Optional[Frame]:
        return None
        
    def disconnect(self):
        pass

class WebcamSource(VideoSource):
    def __init__(self, device_id: int = 0):
        self.device_id = device_id
        
    def connect(self) -> bool:
        return True
        
    def get_frame(self) -> Optional[Frame]:
        return None
        
    def disconnect(self):
        pass
