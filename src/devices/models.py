from sqlalchemy import Column, String, ForeignKey, JSON
from geoalchemy2 import Geometry
from src.core.models import BaseEntity, generate_ulid_like_id

class Device(BaseEntity):
    """
    Base generic device model (Cameras, Sensors, Edge Nodes).
    """
    __tablename__ = "devices"

    id = Column(String, primary_key=True, default=lambda: generate_ulid_like_id("dev"))
    intersection_id = Column(String, ForeignKey("intersections.id"), nullable=False)
    
    device_type = Column(String, nullable=False) # CAMERA, RADAR, EDGE_NODE, SIGNAL_CONTROLLER
    name = Column(String, nullable=False)
    
    ip_address = Column(String, nullable=True)
    mac_address = Column(String, nullable=True)
    
    location = Column(Geometry('POINT', srid=4326), nullable=True)
    
    configuration = Column(JSON, nullable=True)
