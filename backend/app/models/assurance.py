from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class EvidenceObject(Base):
    """B49.3 - Evidence Object"""
    __tablename__ = "assurance_evidence"
    evidence_id = Column(String, primary_key=True)
    subject = Column(String)
    claim_id = Column(String, ForeignKey("assurance_claims.claim_id"))
    evidence_type = Column(String) # E.g., UNIT_TEST, PEN_TEST, HIL_SIMULATION, AUDIT
    methodology = Column(String)
    result = Column(String) # PASS, FAIL, DEGRADED, INCONCLUSIVE
    limitations = Column(JSON)
    valid_from = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    valid_until = Column(DateTime)
    hash_signature = Column(String) # Immutable proof

class PlatformClaim(Base):
    """B49.4 - Claim Registry"""
    __tablename__ = "assurance_claims"
    claim_id = Column(String, primary_key=True)
    subject = Column(String)
    claim_text = Column(String)
    claim_type = Column(String) # PERFORMANCE, SECURITY, SAFETY, COMPLIANCE
    baseline = Column(String)
    status = Column(String) # DESIGNED, IMPLEMENTED, VALIDATED, CERTIFIED

class AssuranceCase(Base):
    """B49.6 - Assurance Case Architecture"""
    __tablename__ = "assurance_cases"
    case_id = Column(String, primary_key=True)
    goal = Column(String)
    system_scope = Column(String)
    claims = Column(JSON) # Array of claim_ids
    arguments = Column(JSON)
    status = Column(String) # DRAFT, UNDER_REVIEW, APPROVED, REJECTED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TestExecutionResult(Base):
    """B49.9 - Test Pyramid (E2E, Integration, Unit, Chaos, DR)"""
    __tablename__ = "assurance_test_results"
    test_id = Column(String, primary_key=True)
    test_type = Column(String) # CHAOS, LOAD, CONTRACT, E2E, DR
    target_component = Column(String)
    execution_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String) # PASS, FAIL
    metrics = Column(JSON) # E.g., Latency, MTTR, RTO
    evidence_id = Column(String, ForeignKey("assurance_evidence.evidence_id"))

class AssuranceFinding(Base):
    """B49.20 - Penetration Testing & Findings"""
    __tablename__ = "assurance_findings"
    finding_id = Column(String, primary_key=True)
    severity = Column(String) # CRITICAL, HIGH, MEDIUM, LOW
    affected_asset = Column(String)
    description = Column(String)
    remediation_plan = Column(String)
    status = Column(String) # OPEN, IN_PROGRESS, RESOLVED, VERIFIED
    deadline = Column(DateTime)
