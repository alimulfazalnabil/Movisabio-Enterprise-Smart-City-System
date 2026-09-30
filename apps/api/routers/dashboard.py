from fastapi import APIRouter, Depends
from security.auth import require_permission
from security.rbac import Permission, Role

router = APIRouter(prefix="/api/v1/dashboard", tags=["Command Center"])

@router.get("/city-overview")
async def get_city_overview(role: Role = Depends(require_permission(Permission.READ_TRAFFIC))):
    """
    Phase 7: City Overview
    Returns high-level aggregation of intersections, congestion, incidents, and alerts.
    """
    return {
        "active_intersections": 42,
        "city_congestion_index": 0.45,
        "active_incidents": 2,
        "critical_alerts": []
    }

@router.get("/intersection/{intersection_id}")
async def get_intersection_view(intersection_id: str, role: Role = Depends(require_permission(Permission.READ_TRAFFIC))):
    """
    Phase 7: Intersection View
    Returns live operational state for the Digital Twin (CesiumJS/deck.gl).
    """
    return {
        "intersection_id": intersection_id,
        "lanes": [],
        "queue_lengths": {"North": 5, "South": 2, "East": 10, "West": 0},
        "current_phase": "East-West",
        "remaining_green_seconds": 12,
        "incidents": []
    }

@router.get("/signal-control/{intersection_id}")
async def get_signal_control_status(intersection_id: str, role: Role = Depends(require_permission(Permission.READ_TRAFFIC))):
    """
    Phase 7: Signal Control Audit
    Displays the strict separation of AI vs Safety vs Controller states.
    """
    return {
        "intersection_id": intersection_id,
        "CURRENT": "East-West GREEN",
        "REQUESTED": "North-South GREEN",     # From AI
        "APPROVED": "North-South GREEN",      # From Safety Engine
        "ACTUAL": "East-West YELLOW"          # From Controller transition
    }
