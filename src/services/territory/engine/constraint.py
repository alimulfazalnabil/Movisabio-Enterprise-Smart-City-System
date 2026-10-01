import uuid
from typing import List, Optional
from src.services.territory.models.schemas import Parcel, PlanningConstraint, ConstraintLevel

class TerritorialConstraintEngine:
    """
    Evaluates spatial constraints against development proposals or parcels.
    """
    
    def evaluate_parcel(self, parcel: Parcel) -> List[PlanningConstraint]:
        constraints = []
        
        # Mock policy evaluation
        if parcel.risk_exposure.get("FLOOD_RISK") == "HIGH":
            constraints.append(
                PlanningConstraint(
                    constraint_id=str(uuid.uuid4()),
                    parcel_id=parcel.parcel_id,
                    constraint_type="FLOOD_RISK",
                    level=ConstraintLevel.CONSTRAINT,
                    description="Parcel intersects high flood risk zone.",
                    policy_reference="ENV_FLD_01"
                )
            )
            
        if parcel.land_use == "PROTECTED_AREA":
            constraints.append(
                PlanningConstraint(
                    constraint_id=str(uuid.uuid4()),
                    parcel_id=parcel.parcel_id,
                    constraint_type="ZONING",
                    level=ConstraintLevel.CONSTRAINT,
                    description="Parcel is a protected environmental area.",
                    policy_reference="ENV_PRO_01"
                )
            )
            
        return constraints
