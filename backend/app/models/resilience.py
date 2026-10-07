from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class TerritorialRisk(Base):
    """B12.1 - Territorial Risk Model"""
    __tablename__ = "territorial_risks"
    risk_id = Column(String, primary_key=True)
    hazard_type = Column(String, index=True)
    location = Column(Geometry('POLYGON'))
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    probability = Column(Float)
    severity = Column(Float)
    consequence = Column(Float)
    confidence = Column(Float)
    affected_assets = Column(JSON)
    status = Column(String) # LOW, MODERATE, HIGH, VERY_HIGH, CRITICAL, UNKNOWN

class EmergencySituation(Base):
    """B12.5 - Emergency Situation Object (Common Operating Picture)"""
    __tablename__ = "emergency_situations"
    situation_id = Column(String, primary_key=True)
    type = Column(String)
    severity = Column(String)
    location = Column(Geometry('GEOMETRY'))
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    confirmed_at = Column(DateTime(timezone=True))
    status = Column(String) # DETECTED, VALIDATING, CONFIRMED, ACTIVE, CONTAINED, RECOVERING, RESOLVED
    affected_services = Column(JSON)
    response_plan_id = Column(String)

class EmergencyResource(Base):
    """B12.17 - Emergency Resource Model"""
    __tablename__ = "emergency_resources"
    resource_id = Column(String, primary_key=True)
    resource_type = Column(String) # Ambulance, Fire Truck, Police, Generator
    location = Column(Geometry('POINT'))
    status = Column(String) # AVAILABLE, DEPLOYED, MAINTENANCE, UNAVAILABLE
    assigned_situation_id = Column(String, ForeignKey("emergency_situations.situation_id"))
    eta_seconds = Column(Integer)

class CriticalServiceStatus(Base):
    """B12.16 - Critical Service Continuity"""
    __tablename__ = "critical_service_status"
    service_id = Column(String, primary_key=True)
    service_type = Column(String) # Power, Water, Healthcare, Telecom
    current_capacity = Column(Float)
    required_capacity = Column(Float)
    status = Column(String) # NORMAL, DEGRADED, SEVERELY_DEGRADED, FAILED, RECOVERING
    estimated_recovery_time = Column(DateTime(timezone=True))

class SensorTrust(Base):
    """B12.28 - Sensor Trust Management"""
    __tablename__ = "sensor_trusts"
    sensor_id = Column(String, primary_key=True)
    reliability = Column(Float)
    historical_accuracy = Column(Float)
    recent_anomalies_count = Column(Integer)
    security_state = Column(String) # SECURE, SUSPICIOUS, COMPROMISED
    trust_score = Column(Float)
    trust_status = Column(String) # TRUSTED, DEGRADED, SUSPICIOUS, OFFLINE
