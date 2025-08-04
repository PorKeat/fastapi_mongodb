from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    productId: str
    name: str
    price: float
    category: str
    description: Optional[str] = None