from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
from datetime import datetime
from app.database import Base

class Listing(Base):
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    quality_grade = Column(String, nullable=True)
    expected_price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    harvest_date = Column(Date, nullable=True)
    selling_window_start = Column(Date, nullable=True)
    selling_window_end = Column(Date, nullable=True)
    is_fpo = Column(Boolean, default=False)
    fpo_id = Column(Integer, ForeignKey("fpos.id"), nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    quality_grade = Column(String, nullable=True)
    budget_per_unit = Column(Float, nullable=False)
    radius_km = Column(Float, nullable=True)
    delivery_by = Column(Date, nullable=True)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    suggested_price = Column(Float, nullable=True)
    distance_km = Column(Float, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
