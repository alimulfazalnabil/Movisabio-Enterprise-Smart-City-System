from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from backend.models.territory import Intersection, TrafficStateObservation

app = FastAPI(
    title="MoviSabio Enterprise API",
    description="Territorial Intelligence & Digital Twin Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Mock Auth Dependency ---
def get_current_tenant():
    # In production: Verify JWT and extract tenant_id
    return "TENANT-CAMPINAS-01"

@app.get("/api/v1/intersections", response_model=List[Intersection])
def get_intersections(tenant_id: str = Depends(get_current_tenant)):
    """Fetch all intersections scoped to the authorized tenant."""
    return [
        Intersection(
            tenant_id=tenant_id,
            intersection_id="INT-001",
            city_id="CAMPINAS-01",
            name="Main & 1st",
            latitude=-22.9099,
            longitude=-47.0626
        )
    ]

@app.get("/api/v1/digital-twin/{intersection_id}/traffic", response_model=TrafficStateObservation)
def get_digital_twin_traffic(intersection_id: str, tenant_id: str = Depends(get_current_tenant)):
    """Digital Twin entrypoint for querying live traffic intelligence."""
    return TrafficStateObservation(
        tenant_id=tenant_id,
        intersection_id=intersection_id,
        timestamp="2026-09-30T18:20:00Z",
        lane_states={
            "N1": {"vehicle_count": 14, "average_speed": 31.4, "queue_length": 8, "confidence": 0.94}
        },
        prediction_confidence=0.92
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
