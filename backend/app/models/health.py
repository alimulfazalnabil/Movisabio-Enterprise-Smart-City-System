from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class HealthcareFacility(Base):
    """B19.3 - Healthcare Facility Intelligence"""
    __tablename__ = "healthcare_facilities"
    facility_id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String) # Hospital, Clinic, Pharmacy
    location = Column(Geometry('POINT'))
    total_beds = Column(Integer)
    available_beds = Column(Integer)
    icu_capacity = Column(Integer)
    available_icu = Column(Integer)
    emergency_capacity_status = Column(String) # NORMAL, SURGE, CRITICAL, OVERFLOW

class DiseaseSignal(Base):
    """B19.9 - Epidemiological Signal Detection"""
    __tablename__ = "disease_signals"
    signal_id = Column(String, primary_key=True)
    signal_type = Column(String) # Respiratory, Gastrointestinal, Vector-borne
    population_zone_id = Column(String)
    aggregate_count = Column(Integer)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    anomaly_score = Column(Float)

class PublicHealthEvent(Base):
    """B19.8 - Public Health Event Intelligence"""
    __tablename__ = "public_health_events"
    event_id = Column(String, primary_key=True)
    event_type = Column(String) # Disease Cluster, Environmental Exposure
    affected_zone = Column(Geometry('POLYGON'))
    severity = Column(String)
    status = Column(String) # DETECTED, VALIDATING, ASSESSED, CONFIRMED, MONITORED, RESOLVED

class Ambulance(Base):
    """B19.7 - Ambulance & Emergency Fleet Intelligence"""
    __tablename__ = "ambulances"
    vehicle_id = Column(String, primary_key=True)
    location = Column(Geometry('POINT'))
    status = Column(String) # AVAILABLE, DISPATCHED, EN_ROUTE, AT_SCENE, TRANSPORTING, AT_HOSPITAL
    current_mission_id = Column(String, nullable=True)
