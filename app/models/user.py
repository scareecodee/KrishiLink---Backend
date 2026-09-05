from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Date, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class UserType(str, enum.Enum):
    farmer = "farmer"
    buyer = "buyer"
    fpo = "fpo"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    phone = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    verified = Column(Boolean, default=False)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    farmer_profile = relationship("FarmerProfile", back_populates="user", uselist=False)
    buyer_profile = relationship("BuyerProfile", back_populates="user", uselist=False)

class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    farm_size = Column(Float, nullable=True)
    experience_years = Column(Integer, nullable=True)
    bank_account_details = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)
    crops_grown = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="farmer_profile")

class BuyerProfile(Base):
    __tablename__ = "buyer_profiles"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    business_name = Column(String, nullable=True)
    business_type = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    preferred_crops = Column(JSON, nullable=True)
    annual_volume = Column(Float, nullable=True)
    
    user = relationship("User", back_populates="buyer_profile")

class FPO(Base):
    __tablename__ = "fpos"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    registration_number = Column(String, nullable=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    farmer_count = Column(Integer, default=0)
    total_production = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
