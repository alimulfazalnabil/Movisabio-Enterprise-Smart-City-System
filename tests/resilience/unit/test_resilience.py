from src.services.resilience.models.schemas import HazardEvent, ExposureEntity, AssetDependency
from src.services.resilience.engine.risk_assessment import RiskAssessmentEngine
from src.services.resilience.engine.cascading_impact import CascadingImpactEngine

def test_risk_assessment():
    engine = RiskAssessmentEngine()
    
    hazard = HazardEvent(
        hazard_id="HZ-1",
        hazard_type="CYCLONE",
        status="ACTIVE",
        intensity=0.9,
        confidence=0.95
    )
    
    # Highly vulnerable, critical hospital
    hospital = ExposureEntity(
        entity_id="HOSP-1",
        entity_type="HOSPITAL",
        criticality="C4",
        vulnerability_score=0.8
    )
    
    risk_hosp = engine.evaluate_risk(hazard, hospital)
    assert risk_hosp.risk_level == "CRITICAL" # 0.9 * 0.8 * 3.0 = 2.16
    
    # Low vulnerability, low criticality warehouse
    warehouse = ExposureEntity(
        entity_id="WH-1",
        entity_type="WAREHOUSE",
        criticality="C1",
        vulnerability_score=0.2
    )
    
    risk_wh = engine.evaluate_risk(hazard, warehouse)
    assert risk_wh.risk_level == "WATCH" # 0.9 * 0.2 * 1.0 = 0.18

def test_cascading_impact():
    risk_engine = RiskAssessmentEngine()
    cascade_engine = CascadingImpactEngine()
    
    hazard = HazardEvent(
        hazard_id="HZ-2",
        hazard_type="FLOOD",
        status="ACTIVE",
        intensity=1.0,
        confidence=0.9
    )
    
    # Primary failure: Substation floods
    substation = ExposureEntity(
        entity_id="SUB-1",
        entity_type="POWER_STATION",
        criticality="C3",
        vulnerability_score=0.9
    )
    risk_sub = risk_engine.evaluate_risk(hazard, substation)
    assert risk_sub.risk_level == "VERY_HIGH"
    
    # Dependencies: Hospital depends on Substation
    deps = [
        AssetDependency(
            source_entity_id="HOSP-2",
            target_entity_id="SUB-1",
            relationship_type="DEPENDS_ON",
            criticality="C4"
        )
    ]
    
    cascades = cascade_engine.evaluate_cascade(risk_sub, deps)
    
    assert len(cascades) == 1
    assert cascades[0].impacted_entity_id == "HOSP-2"
    assert cascades[0].severity == "SEVERE"
