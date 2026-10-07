from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class AgentIdentity(Base):
    """B39.1 - Territorial Agent Architecture"""
    __tablename__ = "agent_identities"
    agent_id = Column(String, primary_key=True)
    agent_name = Column(String)
    agent_role = Column(String) # OPTIMIZER, OBSERVER, COORDINATOR, GOVERNANCE, EXECUTION
    geographic_scope = Column(String)
    risk_level = Column(String) # R0 to R5
    capabilities = Column(JSON) # e.g. ["SignalControl", "TrafficPrediction"]
    is_active = Column(Boolean, default=True)

class AgentProposal(Base):
    """B39.5 - Objective Resolution"""
    __tablename__ = "agent_proposals"
    proposal_id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey("agent_identities.agent_id"))
    territory_id = Column(String)
    proposed_action = Column(JSON)
    objective_metrics = Column(JSON) # e.g. {"congestion_reduction": 0.15, "emissions_increase": 0.02}
    status = Column(String) # PENDING, APPROVED, REJECTED, CONFLICT

class AgentActionLedger(Base):
    """B39.17 - Agent Observability"""
    __tablename__ = "agent_action_ledger"
    ledger_id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey("agent_identities.agent_id"))
    proposal_id = Column(String, ForeignKey("agent_proposals.proposal_id"), nullable=True)
    action_type = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    safety_gateway_status = Column(String) # PASSED, REJECTED
    execution_status = Column(String) # SUCCESS, FAIL, ROLLBACK
    audit_trail = Column(JSON)
