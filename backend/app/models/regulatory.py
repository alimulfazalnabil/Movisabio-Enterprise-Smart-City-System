from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class Regulation(Base):
    """B28.1 - Regulatory Intelligence Foundation"""
    __tablename__ = "regulations"
    regulation_id = Column(String, primary_key=True)
    title = Column(String)
    issuing_authority = Column(String)
    jurisdiction = Column(String)
    effective_from = Column(DateTime(timezone=True))
    version = Column(String)
    status = Column(String) # ACTIVE, SUPERSEDED, DRAFT

class ComplianceRequirement(Base):
    """B28.10 - Compliance Object"""
    __tablename__ = "compliance_requirements"
    requirement_id = Column(String, primary_key=True)
    regulation_id = Column(String, ForeignKey("regulations.regulation_id"))
    subject = Column(String) # e.g. "Industrial Factory", "Building"
    obligation = Column(String)
    evidence_required = Column(String)
    status = Column(String) # COMPLIANT, NON_COMPLIANT, UNKNOWN

class Permit(Base):
    """B28.12 - Permit Intelligence"""
    __tablename__ = "permits"
    permit_id = Column(String, primary_key=True)
    type = Column(String) # BUILDING, ENVIRONMENTAL, WATER
    authority = Column(String)
    holder = Column(String)
    location_id = Column(String)
    issue_date = Column(DateTime(timezone=True))
    expiry_date = Column(DateTime(timezone=True))
    status = Column(String) # ACTIVE, EXPIRING, UNDER_REVIEW
