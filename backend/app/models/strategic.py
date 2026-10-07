from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class GeopoliticalNode(Base):
    """B32.1 - Strategic Intelligence Model"""
    __tablename__ = "geopolitical_nodes"
    node_id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String) # STATE, REGION, ECONOMIC_BLOC
    economic_scale = Column(Float)

class StrategicDependency(Base):
    """B32.3 - Strategic Dependency Intelligence"""
    __tablename__ = "strategic_dependencies"
    dependency_id = Column(String, primary_key=True)
    source_node_id = Column(String, ForeignKey("geopolitical_nodes.node_id"))
    target_node_id = Column(String, ForeignKey("geopolitical_nodes.node_id"))
    domain = Column(String) # ENERGY, FOOD, CRITICAL_MINERALS, TECHNOLOGY
    concentration_pct = Column(Float)
    substitutability = Column(String) # HIGH, MEDIUM, LOW
    criticality = Column(String) # HIGH, MEDIUM, LOW

class GeopoliticalEvent(Base):
    """B32.12 - Geopolitical Event Intelligence"""
    __tablename__ = "geopolitical_events"
    event_id = Column(String, primary_key=True)
    type = Column(String) # SANCTION_EVENT, ENERGY_SHOCK, CONFLICT_EVENT
    description = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime(timezone=True))
    affected_nodes = Column(JSON) # List of node_ids

class CascadingRiskScenario(Base):
    """B32.15 - Cascading Risk Engine"""
    __tablename__ = "cascading_risk_scenarios"
    scenario_id = Column(String, primary_key=True)
    trigger_event_id = Column(String, ForeignKey("geopolitical_events.event_id"))
    propagation_graph = Column(JSON)
    economic_impact_est = Column(Float)
