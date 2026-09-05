from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models.user import User, BuyerProfile
from app.models.listing import Requirement
from app.models.order import Order
from app.schemas.listing import RequirementCreate, RequirementResponse
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.utils.security import require_role
from app.services import matching_service

router = APIRouter(prefix="/api/buyer", tags=["Buyer"])

@router.post("/requirement", response_model=RequirementResponse)
async def create_requirement(req: RequirementCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    new_req = Requirement(**req.model_dump(), buyer_id=current_user.id)
    db.add(new_req)
    await db.commit()
    await db.refresh(new_req)
    return new_req

@router.get("/requirements", response_model=List[RequirementResponse])
async def get_requirements(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    res = await db.execute(select(Requirement).filter(Requirement.buyer_id == current_user.id))
    return res.scalars().all()

@router.put("/requirement/{id}", response_model=RequirementResponse)
async def update_requirement(id: int, req: RequirementCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    db_req = (await db.execute(select(Requirement).filter(Requirement.id == id, Requirement.buyer_id == current_user.id))).scalars().first()
    if db_req:
        for k, v in req.model_dump().items():
            setattr(db_req, k, v)
        await db.commit()
        await db.refresh(db_req)
    return db_req

@router.delete("/requirement/{id}")
async def delete_requirement(id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    db_req = (await db.execute(select(Requirement).filter(Requirement.id == id, Requirement.buyer_id == current_user.id))).scalars().first()
    if db_req:
        db_req.status = "deleted"
        await db.commit()
    return {"msg": "Deleted"}

@router.get("/farmer-matches")
async def get_farmer_matches(requirement_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    return await matching_service.find_farmer_matches(db, requirement_id)

@router.post("/order", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    new_order = Order(**order.model_dump(), total_amount=order.quantity * order.price_per_unit)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    res = await db.execute(select(Order).filter(Order.buyer_id == current_user.id))
    return res.scalars().all()

@router.put("/order/{id}/status", response_model=OrderResponse)
async def update_order_status(id: int, update: OrderStatusUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    order = (await db.execute(select(Order).filter(Order.id == id, Order.buyer_id == current_user.id))).scalars().first()
    if order:
        order.status = update.status
        await db.commit()
        await db.refresh(order)
    return order

@router.get("/profile")
async def get_profile(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    res = await db.execute(select(BuyerProfile).filter(BuyerProfile.user_id == current_user.id))
    return res.scalars().first()

@router.put("/profile")
async def update_profile(profile_data: dict, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_role("buyer"))):
    prof = (await db.execute(select(BuyerProfile).filter(BuyerProfile.user_id == current_user.id))).scalars().first()
    if prof:
        for k, v in profile_data.items():
            setattr(prof, k, v)
        await db.commit()
    return prof
