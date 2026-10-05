from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel

class LogisticsFacility(BaseModel):
    facility_id: str
    facility_type: str # WAREHOUSE, PORT, DISTRIBUTION_CENTER
    capacity: int
    current_load: int
    truck_queue_length: int
    status: str
    location: str

class FreightShipment(BaseModel):
    shipment_id: str
    origin_facility_id: str
    destination_zone: str
    volume: float
    required_temperature: Optional[float]
    delivery_window_start: datetime
    delivery_window_end: datetime
    priority: str

class LoadingZone(BaseModel):
    zone_id: str
    status: str # AVAILABLE, OCCUPIED, RESERVED
    capacity: int
    current_occupancy: int
    
class LogisticsDisruption(BaseModel):
    disruption_id: str
    event_type: str
    severity: str
    affected_nodes: List[str]
    timestamp: datetime
