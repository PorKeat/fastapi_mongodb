from fastapi import APIRouter, HTTPException
from typing import List
from ..models.order import Order
from ..database import db

router = APIRouter()

@router.get("/", response_model=List[Order])
async def get_all_orders():
    cursor = db["orders"].find()
    return [Order(**doc) async for doc in cursor]

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await db["orders"].find_one({"orderId": order_id})
    if order:
        return Order(**order)
    raise HTTPException(status_code=404, detail="Order not found")

@router.post("/", response_model=Order)
async def create_order(order: Order):
    result = await db["orders"].insert_one(order.dict())
    if result.inserted_id:
        return order
    raise HTTPException(status_code=500, detail="Failed to create order")

@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: str, order: Order):
    result = await db["orders"].replace_one({"orderId": order_id}, order.dict())
    if result.modified_count == 1:
        return order
    raise HTTPException(status_code=404, detail="Order not found or not modified")

@router.delete("/{order_id}")
async def delete_order(order_id: str):
    result = await db["orders"].delete_one({"orderId": order_id})
    if result.deleted_count == 1:
        return {"message": "Order deleted"}
    raise HTTPException(status_code=404, detail="Order not found")
