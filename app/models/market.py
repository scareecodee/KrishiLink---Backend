from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Date, DateTime
from datetime import date, datetime
from app.database import Base

class Market(Base):
    __tablename__ = "markets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    state = Column(String, nullable=True)
    district = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    contact_info = Column(JSON, nullable=True)

class MarketPrice(Base):
    __tablename__ = "market_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    price = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    quality_grade = Column(String, nullable=True)
    date = Column(Date, default=date.today)
    arrival_quantity = Column(Float, nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    modal_price = Column(Float, nullable=True)

class PricePrediction(Base):
    __tablename__ = "price_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)
    prediction_date = Column(Date, nullable=False)
    predicted_price = Column(Float, nullable=False)
    confidence_lower = Column(Float, nullable=True)
    confidence_upper = Column(Float, nullable=True)
    factors_impacting = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
