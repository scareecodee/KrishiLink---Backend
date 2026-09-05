from pydantic import BaseModel
from typing import Optional, List

class CropBase(BaseModel):
    name: str
    category: str
    variety: Optional[str] = None
    seasons: Optional[List[str]] = None
    avg_price: Optional[float] = None
    unit: str = "quintal"

class CropCreate(CropBase):
    pass

class CropResponse(CropBase):
    id: int

    class Config:
        from_attributes = True
