from pydantic import BaseModel
from datetime import datetime

class Payment(BaseModel):
    paymentId: str
    customerId: str
    amount: float
    paymentDate: datetime
    method: str