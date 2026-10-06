from src.platform.governance.architecture.adr import ArchitectureAuthority, ArchitectureDecisionRecord, ADRStatus
from src.platform.governance.architecture.conformance import ConformanceEngine, ArchitectureConformance, ConformanceStatus
from src.platform.governance.risk.exceptions import ExceptionEngine, ArchitectureException, ExceptionStatus
from src.platform.governance.technology.portfolio import TechnologyPortfolio, TechnologyItem, TechnologyStatus

def test_architecture_authority():
    auth = ArchitectureAuthority()
    adr = ArchitectureDecisionRecord(
        adr_id="ADR-042",
        title="PostgreSQL as Source of Truth",
        decision="Use PostGIS",
        context="Need geospatial transactions"
    )
    auth.propose_adr(adr)
    
    updated = auth.review_adr("ADR-042", ADRStatus.ACCEPTED)
    assert updated.status == ADRStatus.ACCEPTED

def test_conformance_engine():
    engine = ConformanceEngine()
    conf = ArchitectureConformance(
        service_id="traffic-opt",
        standard_id="STD-API-01",
        status=ConformanceStatus.COMPLIANT
    )
    engine.record_conformance(conf)
    
    fitness = engine.evaluate_fitness("traffic-opt")
    assert fitness["STD-API-01"] == ConformanceStatus.COMPLIANT

def test_exception_engine():
    engine = ExceptionEngine()
    exc = ArchitectureException(
        exception_id="EXC-001",
        requester="regional-team",
        standard_violated="STD-SEC-02",
        reason="Legacy hardware constraint",
        mitigation="VPC isolation"
    )
    engine.request_exception(exc)
    
    updated = engine.review_exception("EXC-001", ExceptionStatus.APPROVED)
    assert updated.status == ExceptionStatus.APPROVED

def test_technology_portfolio():
    portfolio = TechnologyPortfolio()
    tech = TechnologyItem(
        tech_id="tech-1",
        name="Framework X",
        domain="Frontend"
    )
    portfolio.add_technology(tech)
    
    updated = portfolio.update_status("tech-1", TechnologyStatus.EXPERIMENTAL)
    assert updated.status == TechnologyStatus.EXPERIMENTAL
