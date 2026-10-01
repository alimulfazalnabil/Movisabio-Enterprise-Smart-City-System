import uuid
from datetime import datetime, timezone
from typing import Optional
from src.services.v2x.models.schemas import CooperativeObject, CollisionRiskCandidate

class CollisionRiskEngine:
    """
    Evaluates trajectories of cooperative objects to emit collision risk candidates.
    """
    
    def evaluate_risk(self, obj_a: CooperativeObject, obj_b: CooperativeObject) -> Optional[CollisionRiskCandidate]:
        """
        Simplified TTC (Time-To-Collision) calculation.
        """
        # A true implementation projects velocity vectors and computes intersection geometry.
        # This mock simply compares positions and speeds directly (assuming 1D head-on collision for test).
        
        # Distance calculation (highly simplified scalar distance)
        dist = abs(obj_a.position["latitude"] - obj_b.position["latitude"]) * 111000 # Roughly meters
        
        # Relative speed (assuming head on)
        rel_speed = obj_a.velocity_mps + obj_b.velocity_mps
        
        if rel_speed <= 0.1:
            return None # Not moving towards each other fast enough
            
        ttc = dist / rel_speed
        
        if ttc < 5.0: # 5 seconds threshold
            return CollisionRiskCandidate(
                risk_id=str(uuid.uuid4()),
                object_a_id=obj_a.object_id,
                object_b_id=obj_b.object_id,
                time_to_collision_sec=ttc,
                conflict_point={"latitude": (obj_a.position["latitude"] + obj_b.position["latitude"])/2, "longitude": 0.0},
                confidence=obj_a.confidence * obj_b.confidence,
                timestamp=datetime.now(timezone.utc)
            )
            
        return None
