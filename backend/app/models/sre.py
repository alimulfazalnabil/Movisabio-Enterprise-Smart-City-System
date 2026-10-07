from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class ServiceSLO(Base):
    """B45.24 - Domain-Specific SLOs & B45.25 - Service Level Objectives"""
    __tablename__ = "service_slos"
    slo_id = Column(String, primary_key=True)
    service_name = Column(String) # e.g. "traffic_state_api", "agent_runtime"
    sli_metric = Column(String) # e.g. "success_rate_p99", "latency_ms_p95"
    target_value = Column(Float)
    current_value = Column(Float)
    error_budget_remaining = Column(Float)
    status = Column(String) # HEALTHY, DEGRADED, BUDGET_EXHAUSTED
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class PlatformIncident(Base):
    """B45.27 - Incident Management"""
    __tablename__ = "platform_incidents"
    incident_id = Column(String, primary_key=True)
    severity = Column(String) # SEV-1, SEV-2, SEV-3, SEV-4
    title = Column(String)
    affected_services = Column(JSON)
    status = Column(String) # DETECTED, CONTAINED, RECOVERED, POSTMORTEM
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime, nullable=True)

class ZeroTrustPolicy(Base):
    """B45.1 - Security Architecture & B45.16 - Agent Security"""
    __tablename__ = "zero_trust_policies"
    policy_id = Column(String, primary_key=True)
    identity_type = Column(String) # HUMAN, AGENT, IOT_DEVICE, MICROSERVICE
    identity_id = Column(String)
    allowed_scopes = Column(JSON)
    context_requirements = Column(JSON) # e.g. {"mfa": true, "network": "internal"}
    is_active = Column(Boolean, default=True)
