from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models.crop import Crop
from app.models.market import Market, MarketPrice
from app.schemas.crop import CropResponse
from app.schemas.market import MarketResponse
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api", tags=["Common"])

@router.get("/crops", response_model=List[CropResponse])
async def list_crops(search: str = None, db: AsyncSession = Depends(get_db)):
    q = select(Crop)
    if search:
        q = q.filter(Crop.name.ilike(f"%{search}%"))
    res = await db.execute(q)
    return res.scalars().all()

@router.get("/markets", response_model=List[MarketResponse])
async def list_markets(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Market))
    return res.scalars().all()

@router.get("/markets/{id}/prices")
async def get_market_prices_hist(id: int, crop_id: int = None, db: AsyncSession = Depends(get_db)):
    q = select(MarketPrice).filter(MarketPrice.market_id == id)
    if crop_id:
        q = q.filter(MarketPrice.crop_id == crop_id)
    res = await db.execute(q.limit(30))
    return res.scalars().all()

@router.get("/demand/analysis")
async def get_demand_analysis(db: AsyncSession = Depends(get_db)):
    return {"total_requirement_qty": 5000, "open_requirements_count": 25}

@router.post("/logistics/estimate")
async def estimate_logistics(data: dict):
    dist = data.get("distance_km", 0)
    weight = data.get("weight_kg", 0)
    cost = dist * 8 + (weight * 0.1)
    return {"estimated_cost": cost}

@router.get("/notifications")
async def get_notifications(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return []

@router.put("/notifications/{id}/read")
async def mark_notification_read(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"msg": "Read"}

@router.get("/health")
async def health_check():
    import datetime
    return {"status": "ok", "timestamp": datetime.datetime.utcnow()}
