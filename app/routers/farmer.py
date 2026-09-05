from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models.user import User, FarmerProfile
from app.models.listing import Listing
from app.models.order import Order
from app.schemas.listing import ListingCreate, ListingResponse
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.security import require_role
from app.services import price_service, matching_service

router = APIRouter(prefix="/api/farmer", tags=["Farmer"])

@router.post("/listing", response_model=ListingResponse)
async def create_listing(listing: ListingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    new_listing = Listing(**listing.model_dump(), user_id=current_user.id)
    db.add(new_listing)
    await db.commit()
    await db.refresh(new_listing)
    return new_listing

@router.get("/listings", response_model=List[ListingResponse])
async def get_listings(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    res = await db.execute(select(Listing).filter(Listing.user_id == current_user.id))
    return res.scalars().all()

@router.put("/listing/{id}", response_model=ListingResponse)
async def update_listing(id: int, listing: ListingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    db_list = (await db.execute(select(Listing).filter(Listing.id == id, Listing.user_id == current_user.id))).scalars().first()
    if db_list:
        for k, v in listing.model_dump().items():
            setattr(db_list, k, v)
        await db.commit()
        await db.refresh(db_list)
    return db_list

@router.delete("/listing/{id}")
async def delete_listing(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    db_list = (await db.execute(select(Listing).filter(Listing.id == id, Listing.user_id == current_user.id))).scalars().first()
    if db_list:
        db_list.status = "expired"
        await db.commit()
    return {"msg": "Listing marked as expired"}

@router.get("/market-prices")
async def get_market_prices(crop_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    lat = current_user.latitude or 19.076
    lon = current_user.longitude or 72.877
    return await price_service.get_nearby_market_prices(db, crop_id, lat, lon)

@router.get("/buyer-matches")
async def get_buyer_matches(listing_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    return await matching_service.find_buyer_matches(db, listing_id)

@router.post("/order", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    new_order = Order(**order.model_dump(), total_amount=order.quantity * order.price_per_unit)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    res = await db.execute(select(Order).filter(Order.farmer_id == current_user.id))
    return res.scalars().all()

@router.get("/analytics")
async def get_analytics(current_user: User = Depends(require_role("farmer"))):
    return {"revenue": 50000, "active_listings": 3}

@router.get("/profile")
async def get_profile(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    res = await db.execute(select(FarmerProfile).filter(FarmerProfile.user_id == current_user.id))
    return res.scalars().first()

@router.put("/profile")
async def update_profile(profile_data: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("farmer"))):
    prof = (await db.execute(select(FarmerProfile).filter(FarmerProfile.user_id == current_user.id))).scalars().first()
    if prof:
        for k, v in profile_data.items():
            setattr(prof, k, v)
        await db.commit()
    return prof
