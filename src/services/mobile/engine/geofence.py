from typing import Dict, Any
from src.services.mobile.models.schemas import AssetTelemetry, GeofenceZone

class GeofenceEngine:
    """
    Evaluates asset telemetry against geofence boundaries to determine safety state.
    """
    
    def evaluate_position(self, telemetry: AssetTelemetry, zone: GeofenceZone) -> str:
        """
        Determines the state of the asset relative to the zone.
        States: INSIDE_ALLOWED_ZONE, BOUNDARY_WARNING, BREACH_DETECTED
        """
        # A true implementation would use PostGIS or shapely to check Point-in-Polygon
        # Mock logic based on simple bounding box for testing
        
        lat = telemetry.latitude
        lon = telemetry.longitude
        
        # Mock bounding box for zone: 
        # let's assume zone covers lat: 20-25, lon: 85-95
        
        if zone.zone_type == "ALLOWED":
            if 21 <= lat <= 24 and 86 <= lon <= 94:
                return "INSIDE_ALLOWED_ZONE"
            elif 20 <= lat <= 25 and 85 <= lon <= 95:
                return "BOUNDARY_WARNING"
            else:
                return "BREACH_DETECTED"
                
        elif zone.zone_type == "PROHIBITED":
            if 20 <= lat <= 25 and 85 <= lon <= 95:
                return "BREACH_DETECTED"
            else:
                return "SAFE_DISTANCE"
                
        return "UNKNOWN"
