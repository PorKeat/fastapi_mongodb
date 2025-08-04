from fastapi import APIRouter, HTTPException
from typing import List
from ..models.order import Order
from ..database import db
from ..utils.order_utils import orders_util

router = APIRouter()

@router.get("/orders", response_model=List[dict])
async def get_all_orders():
    orders_cursor = db["orders"].find()
    orders_list = []
    async for order in orders_cursor:
        orders_list.append(orders_util(order))
    return orders_list

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await db["orders"].find_one({"orderId": order_id})
    if order:
        return orders_util(order)
    raise HTTPException(status_code=404, detail="Order not found")