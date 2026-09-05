from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class OrderBase(BaseModel):
    match_id: Optional[int] = None
    farmer_id: int
    buyer_id: int
    crop_id: int
    quantity: float
    unit: str
    price_per_unit: float
    quality_grade: Optional[str] = None
    delivery_address: Optional[str] = None
    expected_delivery: Optional[date] = None

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    total_amount: float
    status: str
    payment_status: str
    payment_method: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str

class LogisticsResponse(BaseModel):
    id: int
    order_id: int
    provider_name: Optional[str]
    vehicle_type: Optional[str]
    tracking_number: Optional[str]
    estimated_cost: Optional[float]
    pickup_date: Optional[date]
    delivery_date: Optional[date]
    status: str
    notes: Optional[str]

    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: int
    order_id: int
    user_id: int
    amount: float
    transaction_type: str
    payment_method: Optional[str]
    transaction_id: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
