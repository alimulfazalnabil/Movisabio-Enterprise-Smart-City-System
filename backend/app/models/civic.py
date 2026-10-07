from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class CitizenRecord(Base):
    """B13.1 - Civic Data Model (Minimally viable identity)"""
    __tablename__ = "citizen_records"
    citizen_id = Column(String, primary_key=True)
    tenant_id = Column(String, index=True)
    consent_state = Column(String) # GRANTED, DENIED, WITHDRAWN
    data_classification = Column(String) # RESTRICTED, SENSITIVE
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PublicService(Base):
    """B13.2 - Government Service Catalog"""
    __tablename__ = "public_services"
    service_id = Column(String, primary_key=True)
    name = Column(String)
    provider_agency = Column(String)
    jurisdiction = Column(String)
    sla_hours = Column(Integer)
    status = Column(String) # ACTIVE, SUSPENDED

class ServiceRequest(Base):
    """B13.3 - Service Request Platform"""
    __tablename__ = "service_requests"
    request_id = Column(String, primary_key=True)
    citizen_id = Column(String, ForeignKey("citizen_records.citizen_id"))
    service_id = Column(String, ForeignKey("public_services.service_id"))
    location = Column(Geometry('POINT'))
    status = Column(String) # SUBMITTED, VALIDATING, IN_PROGRESS, RESOLVED, CLOSED
    priority = Column(String)
    assigned_team = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    sla_deadline = Column(DateTime(timezone=True))
    resolution_status = Column(String)

class ConsentRecord(Base):
    """B13.6 - Consent & Data Minimization"""
    __tablename__ = "consent_records"
    consent_id = Column(String, primary_key=True)
    citizen_id = Column(String, ForeignKey("citizen_records.citizen_id"))
    purpose = Column(String)
    data_category = Column(String)
    status = Column(String) # GRANTED, DENIED, EXPIRED
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PublicFacility(Base):
    """B13.21 - Public Facility Intelligence"""
    __tablename__ = "public_facilities"
    facility_id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String) # Hospital, School, Library
    location = Column(Geometry('POINT'))
    capacity = Column(Integer)
    occupancy = Column(Integer)
    operating_status = Column(String)
