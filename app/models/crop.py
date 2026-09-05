from sqlalchemy import Column, Integer, String, Float, JSON
from app.database import Base

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False)
    variety = Column(String, nullable=True)
    seasons = Column(JSON, nullable=True)
    avg_price = Column(Float, nullable=True)
    unit = Column(String, default="quintal")
