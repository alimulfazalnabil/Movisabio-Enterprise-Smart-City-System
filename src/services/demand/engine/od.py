import uuid
from typing import List, Dict
from datetime import datetime, timezone
from src.services.demand.models.schemas import ODMatrix, MobilityDemand

class ODEstimator:
    """
    Estimates Origin-Destination matrices from aggregated demand flows.
    """
    
    def generate_matrix(self, demands: List[MobilityDemand], zones: List[str]) -> ODMatrix:
        """
        Aggregates individual MobilityDemand records into a structured OD Matrix.
        """
        matrix: Dict[str, Dict[str, int]] = {z: {dz: 0 for dz in zones} for z in zones}
        
        for demand in demands:
            if demand.origin_zone in matrix and demand.destination_zone in matrix[demand.origin_zone]:
                matrix[demand.origin_zone][demand.destination_zone] += demand.volume_estimate
                
        time_window = "UNKNOWN"
        if demands:
            time_window = f"{demands[0].time_window_start.strftime('%H:%M')}-{demands[0].time_window_end.strftime('%H:%M')}"
            
        return ODMatrix(
            matrix_id=str(uuid.uuid4()),
            time_window=time_window,
            zones=zones,
            flow_matrix=matrix,
            timestamp=datetime.now(timezone.utc)
        )
