from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.listing import Listing, Requirement, Match
from app.ml.buyer_matcher import BuyerMatcher
from app.models.user import User

matcher = BuyerMatcher()

async def find_buyer_matches(db: AsyncSession, listing_id: int):
    listing = (await db.execute(select(Listing).filter(Listing.id == listing_id))).scalars().first()
    if not listing:
        return []
    
    reqs_res = await db.execute(select(Requirement).filter(Requirement.crop_id == listing.crop_id, Requirement.status == 'open'))
    reqs = reqs_res.scalars().all()
    
    matches = matcher.find_matches(listing, reqs)
    out = []
    for req, score, dist in matches:
        buyer = (await db.execute(select(User).filter(User.id == req.buyer_id))).scalars().first()
        out.append({
            "requirement_id": req.id,
            "buyer_name": buyer.full_name if buyer else "Unknown",
            "score": score,
            "distance_km": dist,
            "budget": req.budget_per_unit
        })
    return out

async def find_farmer_matches(db: AsyncSession, requirement_id: int):
    req = (await db.execute(select(Requirement).filter(Requirement.id == requirement_id))).scalars().first()
    if not req:
        return []
    
    list_res = await db.execute(select(Listing).filter(Listing.crop_id == req.crop_id, Listing.status == 'active'))
    listings = list_res.scalars().all()
    
    # We can reuse the matcher
    matches = matcher.find_matches(req, listings) # Re-using same logic but passing req as "listing" for dummy
    # In real app we'd have a specific list matching
    out = []
    for lst, score, dist in matches:
        out.append({
            "listing_id": lst.id,
            "score": score,
            "distance_km": dist
        })
    return out

async def create_match(db: AsyncSession, listing_id: int, requirement_id: int, score: float, distance_km: float):
    match = Match(
        listing_id=listing_id,
        requirement_id=requirement_id,
        match_score=score,
        distance_km=distance_km
    )
    db.add(match)
    await db.commit()
    await db.refresh(match)
    return match
