from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import date, datetime

class MarketBase(BaseModel):
    name: str
    address: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_info: Optional[Any] = None

class MarketCreate(MarketBase):
    pass

class MarketResponse(MarketBase):
    id: int

    class Config:
        from_attributes = True

class MarketPriceBase(BaseModel):
    market_id: int
    crop_id: int
    price: float
    unit: str
    quality_grade: Optional[str] = None
    date: date
    arrival_quantity: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    modal_price: Optional[float] = None

class MarketPriceCreate(MarketPriceBase):
    pass

class MarketPriceResponse(MarketPriceBase):
    id: int

    class Config:
        from_attributes = True

class PricePredictionResponse(BaseModel):
    id: int
    crop_id: int
    market_id: int
    prediction_date: date
    predicted_price: float
    confidence_lower: Optional[float] = None
    confidence_upper: Optional[float] = None
    factors_impacting: Optional[Any] = None
    created_at: datetime

    class Config:
        from_attributes = True
