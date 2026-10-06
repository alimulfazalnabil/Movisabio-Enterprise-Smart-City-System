from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum

class ReadinessGate(str, enum.Enum):
    G0_DESIGN = "G0_DESIGN"
    G1_BUILD = "G1_BUILD"
    G2_FUNCTIONAL = "G2_FUNCTIONAL"
    G3_SECURITY = "G3_SECURITY"
    G4_PERFORMANCE = "G4_PERFORMANCE"
    G5_RESILIENCE = "G5_RESILIENCE"
    G6_AI_VALIDATION = "G6_AI_VALIDATION"
    G7_HIL_SIM = "G7_HIL_SIM"
    G8_SHADOW = "G8_SHADOW"
    G9_PILOT = "G9_PILOT"
    G10_PROD = "G10_PROD"

class ReleaseValidation(BaseModel):
    release_id: str
    current_gate: ReadinessGate = ReadinessGate.G0_DESIGN
    passed_gates: List[ReadinessGate] = Field(default_factory=list)
    blockers: List[str] = Field(default_factory=list)
    
class ReadinessEngine:
    def __init__(self):
        self.releases: Dict[str, ReleaseValidation] = {}
        
    def start_release(self, release_id: str) -> ReleaseValidation:
        validation = ReleaseValidation(release_id=release_id)
        self.releases[release_id] = validation
        return validation
        
    def pass_gate(self, release_id: str, gate: ReadinessGate):
        if release_id not in self.releases:
            raise ValueError("Release not found")
            
        release = self.releases[release_id]
        if gate not in release.passed_gates:
            release.passed_gates.append(gate)
            release.current_gate = gate
            
    def is_production_ready(self, release_id: str) -> bool:
        if release_id not in self.releases:
            return False
        release = self.releases[release_id]
        return ReadinessGate.G10_PROD in release.passed_gates
