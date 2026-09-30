class ObjectTracker:
    """
    Maintains vehicle identities across video frames (e.g., DeepSORT / ByteTrack).
    """
    def __init__(self):
        self.active_tracks = {}
        
    def update(self, raw_detections):
        """
        In production, this applies Kalman filtering and IOU matching.
        """
        # Mock tracking
        tracked_objects = []
        for i, det in enumerate(raw_detections):
            # Assign persistent ID
            track_id = f"VEH-{i}"
            tracked_objects.append({
                "track_id": track_id,
                "class": det.get("class", "car"),
                "confidence": det.get("confidence", 0.90),
                "bbox": det.get("bbox")
            })
        return tracked_objects
