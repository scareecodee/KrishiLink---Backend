from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.utils.security import require_role

router = APIRouter(prefix="/api/fpo", tags=["FPO"])

@router.post("/aggregate")
async def create_aggregated_listing(data: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("fpo"))):
    return {"msg": "Aggregated listing created (stub)"}

@router.get("/listings")
async def get_listings(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("fpo"))):
    return []

@router.post("/farmer/add")
async def add_farmer(data: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("fpo"))):
    return {"msg": "Farmer added to FPO"}

@router.get("/analytics")
async def get_analytics(current_user: User = Depends(require_role("fpo"))):
    return {"total_production": 5000, "active_listings": 10}

@router.get("/profile")
async def get_profile(current_user: User = Depends(require_role("fpo"))):
    return {"name": "FPO Name"}
