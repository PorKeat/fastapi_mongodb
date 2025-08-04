from typing import List
from pydantic import BaseModel
from datetime import datetime

class OrderItem(BaseModel):
    productId: str
    quantity: int
    unitPrice: float

class Order(BaseModel):
    orderId: str
    customerId: str
    orderDate: datetime
    status: str
    orderItems: List[OrderItem]