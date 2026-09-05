from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.order import Transaction
from app.models.crop import Crop
from app.schemas.crop import CropCreate, CropResponse
from app.schemas.market import MarketPriceCreate
from app.utils.security import require_role

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/users")
async def list_users(page: int = 1, size: int = 10, user_type: str = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    q = select(User)
    if user_type:
        q = q.filter(User.user_type == user_type)
    res = await db.execute(q.offset((page-1)*size).limit(size))
    return res.scalars().all()

@router.put("/user/{id}/verify")
async def verify_user(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    user = (await db.execute(select(User).filter(User.id == id))).scalars().first()
    if user:
        user.verified = True
        await db.commit()
    return {"msg": "Verified"}

@router.get("/transactions")
async def list_transactions(page: int = 1, size: int = 10, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    res = await db.execute(select(Transaction).offset((page-1)*size).limit(size))
    return res.scalars().all()

@router.get("/analytics")
async def get_analytics(current_user: User = Depends(require_role("admin"))):
    return {"total_farmers": 100, "total_buyers": 50, "revenue": 100000}

@router.post("/crops", response_model=CropResponse)
async def add_crop(crop: CropCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    new_crop = Crop(**crop.model_dump())
    db.add(new_crop)
    await db.commit()
    await db.refresh(new_crop)
    return new_crop

@router.put("/market-prices")
async def update_market_prices(prices: List[MarketPriceCreate], db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    return {"msg": "Prices updated (stub)"}

@router.get("/disputes")
async def list_disputes(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    return []
