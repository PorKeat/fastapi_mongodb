from pydantic import BaseModel
from typing import Optional

class Room(BaseModel):
    roomId: str
    name: str
    type: str
    pricePerHour: float
    description: Optional[str] = None
    available: bool = True