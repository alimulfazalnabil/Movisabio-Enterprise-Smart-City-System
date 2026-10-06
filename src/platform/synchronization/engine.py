from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone

class SyncRecord(BaseModel):
    sync_id: str
    edge_site_id: str
    object_type: str
    object_id: str
    direction: str # UPLOAD, DOWNLOAD
    object_version: int
    status: str = "PENDING"
    source_timestamp: datetime
    
class SyncEngine:
    def __init__(self):
        self.queue: List[SyncRecord] = []
        
    def enqueue(self, record: SyncRecord) -> None:
        self.queue.append(record)
        
    def process_queue(self, strategy: str = "APPEND") -> List[SyncRecord]:
        """
        Processes the sync queue based on data resolution strategy (e.g. Append-only, Versioned)
        """
        processed = []
        for record in self.queue:
            if record.status == "PENDING":
                record.status = "SYNCHRONIZED"
                record.source_timestamp = datetime.now(timezone.utc)
                processed.append(record)
        return processed
