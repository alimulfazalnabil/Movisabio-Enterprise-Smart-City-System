from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from backend.app.database.session import get_db
from backend.app.models.traffic import TrafficState

router = APIRouter()

@router.get("/intersections/{intersection_id}/traffic-state")
async def get_traffic_state(intersection_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TrafficState)
        .where(TrafficState.intersection_id == intersection_id)
        .order_by(TrafficState.timestamp.desc())
        .limit(1)
    )
    state = result.scalars().first()
    if not state:
        raise HTTPException(status_code=404, detail="Traffic state not found")
        
    return {
        "intersection_id": state.intersection_id,
        "timestamp": state.timestamp,
        "vehicle_count": state.vehicle_count,
        "flow": state.flow,
        "average_speed": state.average_speed,
        "congestion_level": state.congestion_level,
        "lane_states": state.lane_states
    }

@router.get("/intersections/{intersection_id}/traffic-state/history")
async def get_traffic_state_history(intersection_id: str, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TrafficState)
        .where(TrafficState.intersection_id == intersection_id)
        .order_by(TrafficState.timestamp.desc())
        .limit(limit)
    )
    states = result.scalars().all()
    return states
