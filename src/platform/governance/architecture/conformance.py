from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class ConformanceStatus(str, enum.Enum):
    COMPLIANT = "COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    EXEMPTED = "EXEMPTED"
    UNKNOWN = "UNKNOWN"

class ArchitectureConformance(BaseModel):
    service_id: str
    standard_id: str
    status: ConformanceStatus = ConformanceStatus.UNKNOWN
    violations: List[str] = Field(default_factory=list)
    last_checked: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ConformanceEngine:
    def __init__(self):
        self.conformance_records: Dict[str, ArchitectureConformance] = {}
        
    def record_conformance(self, conformance: ArchitectureConformance) -> ArchitectureConformance:
        key = f"{conformance.service_id}::{conformance.standard_id}"
        self.conformance_records[key] = conformance
        return conformance
        
    def evaluate_fitness(self, service_id: str) -> Dict[str, ConformanceStatus]:
        fitness = {}
        for key, record in self.conformance_records.items():
            if record.service_id == service_id:
                fitness[record.standard_id] = record.status
        return fitness
