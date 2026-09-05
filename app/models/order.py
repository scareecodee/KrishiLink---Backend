from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime
from datetime import datetime
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=True)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    quality_grade = Column(String, nullable=True)
    delivery_address = Column(String, nullable=True)
    expected_delivery = Column(Date, nullable=True)
    status = Column(String, default="pending")
    payment_status = Column(String, default="pending")
    payment_method = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Logistics(Base):
    __tablename__ = "logistics"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    provider_name = Column(String, nullable=True)
    vehicle_type = Column(String, nullable=True)
    tracking_number = Column(String, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    pickup_date = Column(Date, nullable=True)
    delivery_date = Column(Date, nullable=True)
    status = Column(String, default="scheduled")
    notes = Column(String, nullable=True)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)
    payment_method = Column(String, nullable=True)
    transaction_id = Column(String, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
