from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class RecoveryPhase(str, enum.Enum):
    DETECT = "DETECT"
    FAILOVER = "FAILOVER"
    RESTORE = "RESTORE"
    VERIFY = "VERIFY"
    RESUME = "RESUME"

class RecoveryDrill(BaseModel):
    drill_id: str
    target_rto_minutes: int
    actual_rto_minutes: Optional[int] = None
    data_verified: bool = False
    successful: bool = False
    
class DREngine:
    def __init__(self):
        self.drills: Dict[str, RecoveryDrill] = {}
        
    def start_drill(self, drill_id: str, target_rto: int) -> RecoveryDrill:
        drill = RecoveryDrill(drill_id=drill_id, target_rto_minutes=target_rto)
        self.drills[drill_id] = drill
        return drill
        
    def complete_drill(self, drill_id: str, actual_rto: int, data_verified: bool) -> RecoveryDrill:
        if drill_id not in self.drills:
            raise ValueError("Drill not found")
            
        drill = self.drills[drill_id]
        drill.actual_rto_minutes = actual_rto
        drill.data_verified = data_verified
        
        if data_verified and actual_rto <= drill.target_rto_minutes:
            drill.successful = True
            
        return drill
