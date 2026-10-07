from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from backend.app.database.session import Base
from datetime import datetime, timezone

class Institution(Base):
    """B30.1 - Government Operating Model"""
    __tablename__ = "institutions"
    institution_id = Column(String, primary_key=True)
    name = Column(String)
    jurisdiction = Column(String)
    type = Column(String) # MINISTRY, AGENCY, MUNICIPALITY
    mandate = Column(String)
    budget_allocated = Column(Float)
    workforce_capacity = Column(Integer)

class PublicService(Base):
    """B30.4 - Public Service Catalog"""
    __tablename__ = "public_services"
    service_id = Column(String, primary_key=True)
    institution_id = Column(String, ForeignKey("institutions.institution_id"))
    name = Column(String)
    category = Column(String) # PERMIT, HEALTH, TRANSIT
    target_sla_days = Column(Integer)
    status = Column(String) # ACTIVE, SUSPENDED

class AdministrativeWorkflow(Base):
    """B30.3 - Government Process Intelligence"""
    __tablename__ = "administrative_workflows"
    workflow_id = Column(String, primary_key=True)
    service_id = Column(String, ForeignKey("public_services.service_id"))
    applicant_id = Column(String)
    current_stage = Column(String)
    submission_date = Column(DateTime(timezone=True))
    sla_breach_risk = Column(String) # LOW, MEDIUM, HIGH, BREACHED
    status = Column(String) # PENDING, APPROVED, REJECTED

class PublicProgram(Base):
    """B30.14 - Public Program Digital Twin"""
    __tablename__ = "public_programs"
    program_id = Column(String, primary_key=True)
    institution_id = Column(String, ForeignKey("institutions.institution_id"))
    name = Column(String)
    budget = Column(Float)
    target_outcomes = Column(JSON)
    status = Column(String) # PLANNING, ACTIVE, COMPLETED
