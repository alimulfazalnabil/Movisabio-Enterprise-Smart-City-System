from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from backend.app.database.session import get_db
from backend.app.models.traffic import Camera

router = APIRouter()

@router.get("/", response_model=List[dict])
async def list_cameras(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Camera))
    cameras = result.scalars().all()
    # Pydantic schemas will be implemented later, returning raw dict for now
    return [{"camera_id": c.camera_id, "site_id": c.site_id, "status": c.status} for c in cameras]

@router.get("/{camera_id}")
async def get_camera(camera_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Camera).where(Camera.camera_id == camera_id))
    camera = result.scalars().first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return {"camera_id": camera.camera_id, "stream_url": camera.stream_url, "status": camera.status}
