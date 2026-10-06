import cv2
from datetime import datetime, timezone

class Frame:
    def __init__(self, frame_id: int, image, timestamp: datetime, camera_id: str):
        self.frame_id = frame_id
        self.image = image
        self.timestamp = timestamp
        self.camera_id = camera_id

class VideoIngestionService:
    def __init__(self, camera_id: str, source: str):
        self.camera_id = camera_id
        self.source = source
        self.cap = cv2.VideoCapture(source)
        self.frame_count = 0

    def get_next_frame(self) -> Frame | None:
        if not self.cap.isOpened():
            return None
        
        ret, frame_image = self.cap.read()
        if not ret:
            return None
            
        self.frame_count += 1
        timestamp = datetime.now(timezone.utc)
        
        return Frame(
            frame_id=self.frame_count,
            image=frame_image,
            timestamp=timestamp,
            camera_id=self.camera_id
        )

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
