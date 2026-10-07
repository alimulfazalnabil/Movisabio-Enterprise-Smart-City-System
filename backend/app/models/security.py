from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class SecurityAsset(Base):
    """B25.1 - Cyber-Physical Security Foundation"""
    __tablename__ = "security_assets"
    asset_id = Column(String, primary_key=True)
    owner = Column(String)
    type = Column(String) # IOT, NETWORK, CLOUD, AI, PHYSICAL
    criticality = Column(String) # C0, C1, C2, C3, C4, C5
    security_posture_score = Column(Float)
    last_assessment = Column(DateTime(timezone=True))

class SecurityEvent(Base):
    """B25.14 - Security Event Fabric"""
    __tablename__ = "security_events"
    event_id = Column(String, primary_key=True)
    timestamp = Column(DateTime(timezone=True))
    source = Column(String)
    asset_id = Column(String, ForeignKey("security_assets.asset_id"))
    event_type = Column(String)
    severity = Column(String)
    confidence = Column(Float)
    evidence = Column(JSON)

class Vulnerability(Base):
    """B25.11 - Vulnerability Intelligence"""
    __tablename__ = "vulnerabilities"
    vuln_id = Column(String, primary_key=True)
    cve_id = Column(String)
    asset_id = Column(String, ForeignKey("security_assets.asset_id"))
    cvss_score = Column(Float)
    status = Column(String) # DETECTED, MITIGATED, PATCHED
    priority_level = Column(String) # CRITICAL, HIGH, MEDIUM, LOW

class CyberPhysicalIncident(Base):
    """B25.20 - Cyber-Physical Incident Lifecycle"""
    __tablename__ = "cyber_physical_incidents"
    incident_id = Column(String, primary_key=True)
    primary_cyber_event_id = Column(String, ForeignKey("security_events.event_id"))
    physical_asset_impacted = Column(String)
    impact_severity = Column(String)
    status = Column(String) # DETECTED, CONTAINING, RESOLVED
