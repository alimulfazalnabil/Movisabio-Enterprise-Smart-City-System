from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum, Boolean, JSON
from geoalchemy2 import Geometry
from backend.app.database.session import Base
from datetime import datetime, timezone

class MobilityEvent(Base):
    """B9.2 - Mobility Event Fabric"""
    __tablename__ = "mobility_events"
    event_id = Column(String, primary_key=True)
    event_type = Column(String, index=True) # e.g. BUS_DELAYED, PARKING_OCCUPIED
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    location = Column(Geometry('POINT'))
    source = Column(String)
    entity_id = Column(String)
    confidence = Column(Float)
    data_quality = Column(String)
    tenant_id = Column(String, index=True)
    correlation_id = Column(String)

class TransitRoute(Base):
    """B9.5 - Smart Public Transit"""
    __tablename__ = "transit_routes"
    route_id = Column(String, primary_key=True)
    agency_id = Column(String)
    mode = Column(String) # Bus, Tram, etc.
    name = Column(String)
    geometry = Column(Geometry('LINESTRING'))

class TransitVehicle(Base):
    """B9.5 - Transit Vehicle State"""
    __tablename__ = "transit_vehicles"
    vehicle_id = Column(String, primary_key=True)
    route_id = Column(String, ForeignKey("transit_routes.route_id"))
    current_location = Column(Geometry('POINT'))
    timestamp = Column(DateTime(timezone=True))
    delay_seconds = Column(Integer)
    occupancy_percentage = Column(Float)
    priority_requested = Column(Boolean, default=False) # B9.6

class ParkingFacility(Base):
    """B9.9 - Smart Parking Intelligence"""
    __tablename__ = "parking_facilities"
    facility_id = Column(String, primary_key=True)
    name = Column(String)
    location = Column(Geometry('POLYGON'))
    capacity = Column(Integer)
    occupancy = Column(Integer) # Note: B9.9 explicitly states to use UNKNOWN/NULL if sensor fails
    status = Column(String) # AVAILABLE, OCCUPIED, RESERVED, UNAVAILABLE, UNKNOWN

class CurbZone(Base):
    """B9.11 - Smart Curb Intelligence"""
    __tablename__ = "curb_zones"
    zone_id = Column(String, primary_key=True)
    designation = Column(String) # Loading zone, Bus stop, Taxi zone
    location = Column(Geometry('LINESTRING'))
    status = Column(String)
    utilization = Column(Float)

class EVCharger(Base):
    """B9.14 - EV Mobility Intelligence"""
    __tablename__ = "ev_chargers"
    charger_id = Column(String, primary_key=True)
    location = Column(Geometry('POINT'))
    capacity_kw = Column(Float)
    status = Column(String) # AVAILABLE, CHARGING, OFFLINE
    current_session_id = Column(String)

class FreightShipment(Base):
    """B9.12 - Urban Freight Intelligence"""
    __tablename__ = "freight_shipments"
    shipment_id = Column(String, primary_key=True)
    vehicle_id = Column(String)
    destination = Column(Geometry('POINT'))
    time_window_start = Column(DateTime(timezone=True))
    time_window_end = Column(DateTime(timezone=True))
    status = Column(String)
    
class ODMatrix(Base):
    """B9.3 - Mobility Demand (Origin-Destination)"""
    __tablename__ = "od_matrices"
    matrix_id = Column(String, primary_key=True)
    timestamp = Column(DateTime(timezone=True))
    time_horizon = Column(String)
    data = Column(JSON) # JSON matrix payload
