from src.platform.assurance.sla.sla_engine import SLAEngine, SLAContract, SLARisk
from src.platform.assurance.outcome.outcome_engine import OutcomeEngine, CustomerOutcome, EvidenceType, OutcomeStatus
from src.platform.value.roi.calculator import ValueEngine, ROIModel
from src.platform.customer_intelligence.health.score import CustomerHealthEngine, HealthScore

def test_sla_engine():
    engine = SLAEngine()
    contract = SLAContract(
        contract_id="c-1",
        service_id="s-1",
        tenant_id="t-1",
        required_availability=99.9,
        current_availability=100.0
    )
    engine.register_contract(contract)
    
    # Evaluate risk
    contract = engine.evaluate_sla("c-1", 99.92, 1, -0.01)
    assert contract.risk_level == SLARisk.HIGH
    
    contract = engine.evaluate_sla("c-1", 99.8, 1, -0.01)
    assert contract.risk_level == SLARisk.BREACHED

def test_outcome_engine():
    engine = OutcomeEngine()
    outcome = CustomerOutcome(
        outcome_id="o-1",
        tenant_id="t-1",
        kpi_name="Intersection Delay",
        baseline_value=120.0,
        target_value=90.0,
        current_value=120.0
    )
    engine.register_outcome(outcome)
    
    # Measure progress
    outcome = engine.measure_outcome("o-1", 96.0, EvidenceType.OBSERVED)
    assert outcome.evidence == EvidenceType.OBSERVED
    assert outcome.status == OutcomeStatus.PARTIALLY_ACHIEVED
    
    outcome = engine.measure_outcome("o-1", 85.0, EvidenceType.OBSERVED)
    assert outcome.status == OutcomeStatus.ACHIEVED

def test_value_engine():
    engine = ValueEngine()
    roi = ROIModel(
        roi_id="roi-1",
        tenant_id="t-1",
        investment=100000.0
    )
    engine.create_roi_model(roi)
    
    roi = engine.update_benefits("roi-1", 50000.0, 75000.0, 25000.0)
    assert roi.total_benefit == 150000.0
    assert roi.roi_percentage == 50.0

def test_customer_health_engine():
    engine = CustomerHealthEngine()
    health = engine.evaluate_health(
        tenant_id="t-1",
        service=0.99,
        sla=0.95,
        adoption=0.4, # Low adoption
        outcome=0.5,
        support=0.9
    )
    assert health.composite_health == HealthScore.STABLE
    
    health = engine.evaluate_health(
        tenant_id="t-2",
        service=0.5,
        sla=0.5,
        adoption=0.2,
        outcome=0.1,
        support=0.5
    )
    assert health.composite_health == HealthScore.CRITICAL
