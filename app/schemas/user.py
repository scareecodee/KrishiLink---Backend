from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime
from app.models.user import UserType

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    user_type: UserType
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    verified: bool
    rating: float
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class FarmerProfileBase(BaseModel):
    farm_size: Optional[float] = None
    experience_years: Optional[int] = None
    bank_account_details: Optional[Any] = None
    certifications: Optional[List[str]] = None
    crops_grown: Optional[List[str]] = None

class FarmerProfileCreate(FarmerProfileBase):
    pass

class FarmerProfileResponse(FarmerProfileBase):
    user_id: int

    class Config:
        from_attributes = True

class BuyerProfileBase(BaseModel):
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    gst_number: Optional[str] = None
    preferred_crops: Optional[List[str]] = None
    annual_volume: Optional[float] = None

class BuyerProfileCreate(BuyerProfileBase):
    pass

class BuyerProfileResponse(BuyerProfileBase):
    user_id: int

    class Config:
        from_attributes = True
