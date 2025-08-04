from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    customerId: str
    name: str
    email: str
    phone: str
    address: str
    membershipId: Optional[str]
