from pydantic import BaseModel
from datetime import datetime

class Membership(BaseModel):
    membershipId: str
    customerId: str
    type: str
    startDate: datetime
    expiryDate: datetime