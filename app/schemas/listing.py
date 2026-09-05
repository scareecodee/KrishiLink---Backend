from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ListingBase(BaseModel):
    crop_id: int
    quantity: float
    unit: str
    quality_grade: Optional[str] = None
    expected_price: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    harvest_date: Optional[date] = None
    selling_window_start: Optional[date] = None
    selling_window_end: Optional[date] = None

class ListingCreate(ListingBase):
    is_fpo: bool = False
    fpo_id: Optional[int] = None

class ListingResponse(ListingBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    is_fpo: bool
    fpo_id: Optional[int] = None

    class Config:
        from_attributes = True

class RequirementBase(BaseModel):
    crop_id: int
    quantity: float
    unit: str
    quality_grade: Optional[str] = None
    budget_per_unit: float
    radius_km: Optional[float] = None
    delivery_by: Optional[date] = None

class RequirementCreate(RequirementBase):
    pass

class RequirementResponse(RequirementBase):
    id: int
    buyer_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class MatchResponse(BaseModel):
    id: int
    listing_id: int
    requirement_id: int
    match_score: float
    suggested_price: Optional[float] = None
    distance_km: Optional[float] = None
    status: str
    created_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True
