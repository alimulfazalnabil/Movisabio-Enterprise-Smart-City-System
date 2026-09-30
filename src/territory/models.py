from sqlalchemy import Column, String, ForeignKey
from geoalchemy2 import Geometry
from src.core.models import BaseEntity, generate_ulid_like_id

class City(BaseEntity):
    """
    Municipal boundary layer.
    """
    __tablename__ = "cities"
    
    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("city"))
    name = Column(String, index=True, nullable=False)
    boundary = Column(Geometry('POLYGON', srid=4326), nullable=True)

class Site(BaseEntity):
    """
    Geographic area within a city (e.g. a specific district, campus, or zone).
    """
    __tablename__ = "sites"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("site"))
    city_id = Column(String, ForeignKey("cities.id"), nullable=False)
    name = Column(String, nullable=False)
    boundary = Column(Geometry('POLYGON', srid=4326), nullable=True)

class Intersection(BaseEntity):
    """
    The fundamental traffic node bridging GIS, Perception, and Control.
    """
    __tablename__ = "intersections"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("int"))
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    
    # Core Spatial Position
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    # Operational configuration
    controller_type = Column(String, nullable=False) # e.g. NTCIP, SCATS, SCOOT, MoviSabioEdge
    ai_mode = Column(String, default="simulation") # simulation, advisory, active_control
    
class Road(BaseEntity):
    """
    Road segment or approach leading to an intersection.
    """
    __tablename__ = "roads"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("road"))
    intersection_id = Column(String, ForeignKey("intersections.id"), nullable=False)
    name = Column(String, nullable=False)
    direction = Column(String, nullable=False) # Northbound, Southbound, etc.
    
    path = Column(Geometry('LINESTRING', srid=4326), nullable=True)
