from typing import List
from src.services.resilience.models.schemas import RiskAssessment, AssetDependency, CascadingEvent
import uuid

class CascadingImpactEngine:
    def evaluate_cascade(self, initial_risk: RiskAssessment, dependencies: List[AssetDependency]) -> List[CascadingEvent]:
        """
        Projects secondary failures caused by an primary asset at risk.
        """
        cascades = []
        
        # If the primary asset is not at high risk, it probably won't cascade yet
        if initial_risk.risk_level not in ["CRITICAL", "VERY_HIGH"]:
            return cascades
            
        for dep in dependencies:
            if dep.target_entity_id == initial_risk.entity_id and dep.relationship_type == "DEPENDS_ON":
                # The source_entity depends on the target_entity (which is at risk)
                # Therefore source_entity is at risk of cascading failure
                severity = "SEVERE" if dep.criticality in ["C3", "C4"] else "MODERATE"
                
                cascades.append(CascadingEvent(
                    event_id=str(uuid.uuid4()),
                    root_event_id=initial_risk.hazard_id,
                    parent_entity_id=dep.target_entity_id,
                    impacted_entity_id=dep.source_entity_id,
                    severity=severity,
                    status="CANDIDATE"
                ))
                
        return cascades
