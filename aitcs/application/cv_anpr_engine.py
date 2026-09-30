"""Adapt precomputed vision detections into AITCS and ANPR domain records."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass(frozen=True)
class ANPRRecord:
    """One recognized plate and its blacklist lookup result."""

    plate_number: str
    confidence: float
    vehicle_type: str
    intersection_id: str
    is_blacklisted: bool
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class VisionDetectionResult:
    """Aggregated object counts and plate detections for one frame."""

    intersection_id: str
    vehicle_count: int
    pedestrian_count: int
    emergency_vehicle_detected: bool
    detected_plates: List[ANPRRecord]
    timestamp: datetime = field(default_factory=datetime.utcnow)

class ComputerVisionANPREngine:
    """Normalize detector output; image inference happens outside this module."""

    def __init__(self, blacklist_db: Optional[List[str]] = None):
        """Create the engine with an optional in-memory list of blocked plates."""

        self.blacklist_db = set(blacklist_db or ["DAH-9941", "MZH-7720", "EX-8821"])

    def process_frame_telemetry(self, intersection_id: str, raw_detections: dict) -> VisionDetectionResult:
        """Convert a detector payload into typed vision and plate records.

        Args:
            intersection_id: Source intersection for every generated record.
            raw_detections: Mapping with counts, emergency flag and a ``plates``
                list. Missing keys receive neutral defaults.

        Returns:
            Normalized counts and ANPR records. The input contains detections;
            this method does not process pixels or perform OCR.
        """
        plates_raw = raw_detections.get("plates", [])
        anpr_records = []
        
        for p in plates_raw:
            plate = p.get("plate", "UNKNOWN")
            conf = float(p.get("confidence", 0.0))
            v_type = p.get("vehicle_type", "SEDAN")
            is_blacklisted = plate in self.blacklist_db
            
            anpr_records.append(ANPRRecord(
                plate_number=plate,
                confidence=conf,
                vehicle_type=v_type,
                intersection_id=intersection_id,
                is_blacklisted=is_blacklisted
            ))

        return VisionDetectionResult(
            intersection_id=intersection_id,
            vehicle_count=int(raw_detections.get("vehicle_count", 0)),
            pedestrian_count=int(raw_detections.get("pedestrian_count", 0)),
            emergency_vehicle_detected=bool(raw_detections.get("emergency_vehicle_detected", False)),
            detected_plates=anpr_records
        )
