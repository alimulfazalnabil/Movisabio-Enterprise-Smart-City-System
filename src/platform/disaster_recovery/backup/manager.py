from datetime import datetime, timezone
from typing import Dict, Optional

class BackupManager:
    def __init__(self):
        self.backups = {}
        
    def create_backup(self, service_id: str, data: bytes) -> str:
        backup_id = f"bkp-{len(self.backups) + 1}"
        self.backups[backup_id] = {
            "service_id": service_id,
            "data": data,
            "timestamp": datetime.now(timezone.utc),
            "status": "COMPLETED"
        }
        return backup_id
        
    def restore(self, backup_id: str) -> Optional[bytes]:
        backup = self.backups.get(backup_id)
        if backup and backup["status"] == "COMPLETED":
            return backup["data"]
        return None
