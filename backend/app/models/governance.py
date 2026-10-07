from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class GovernancePolicy(Base):
    """B46.21 - Policy-as-Code"""
    __tablename__ = "governance_policies"
    policy_id = Column(String, primary_key=True)
    name = Column(String)
    jurisdiction = Column(String)
    policy_type = Column(String) # SOVEREIGNTY, PRIVACY, AI_RISK, RETENTION
    rule_definition = Column(JSON)
    is_active = Column(Boolean, default=True)

class DataAsset(Base):
    """B46.3 - Data Classification & B46.9 - Sovereignty Engine"""
    __tablename__ = "governance_data_assets"
    asset_id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey("global_tenants.tenant_id"))
    classification = Column(String) # PUBLIC, CONFIDENTIAL, SENSITIVE, SOVEREIGN
    purpose_limitation = Column(String)
    legal_basis = Column(String)
    residency = Column(String)
    retention_days = Column(Integer)
    status = Column(String) # VALID, SUSPECT, STALE, ARCHIVED

class AIUseCase(Base):
    """B46.15 - AI Use-Case Registry"""
    __tablename__ = "governance_ai_use_cases"
    use_case_id = Column(String, primary_key=True)
    model_name = Column(String)
    risk_level = Column(String) # AI-R0 to AI-R5
    decision_impact = Column(String)
    human_oversight_required = Column(Boolean)
    evidence_status = Column(String) # CONCEPTUAL, LAB_VALIDATED, PRODUCTION_VALIDATED
    approval_status = Column(String) # PENDING, APPROVED, REJECTED, SUSPENDED

class GovernanceEvidence(Base):
    """B46.24 - Compliance Evidence Store"""
    __tablename__ = "governance_evidence_records"
    evidence_id = Column(String, primary_key=True)
    control_id = Column(String)
    system = Column(String)
    tenant_id = Column(String)
    evidence_payload = Column(JSON)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    valid_until = Column(DateTime, nullable=True)

class DataContract(Base):
    """B46.11 - Data Contracts"""
    __tablename__ = "governance_data_contracts"
    contract_id = Column(String, primary_key=True)
    producer = Column(String)
    consumer = Column(String)
    geographic_scope = Column(String)
    permitted_use = Column(String)
    prohibited_use = Column(String)
    status = Column(String) # ACTIVE, REVOKED, EXPIRED
