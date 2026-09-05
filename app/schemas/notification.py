from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    type: str
    title: str
    message: str
    read: bool
    created_at: datetime
    metadata_info: Optional[Any] = None

    class Config:
        from_attributes = True
