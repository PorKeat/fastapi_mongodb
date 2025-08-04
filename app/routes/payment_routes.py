from fastapi import APIRouter, HTTPException
from typing import List
from ..models.payment import Payment
from ..database import db

router = APIRouter()

@router.get("/", response_model=List[Payment])
async def get_all_payments():
    cursor = db["payments"].find()
    return [Payment(**doc) async for doc in cursor]

@router.get("/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str):
    payment = await db["payments"].find_one({"paymentId": payment_id})
    if payment:
        return Payment(**payment)
    raise HTTPException(status_code=404, detail="Payment not found")

@router.post("/", response_model=Payment)
async def create_payment(payment: Payment):
    result = await db["payments"].insert_one(payment.dict())
    if result.inserted_id:
        return payment
    raise HTTPException(status_code=500, detail="Failed to create payment")

@router.put("/{payment_id}", response_model=Payment)
async def update_payment(payment_id: str, payment: Payment):
    result = await db["payments"].replace_one({"paymentId": payment_id}, payment.dict())
    if result.modified_count == 1:
        return payment
    raise HTTPException(status_code=404, detail="Payment not found or not modified")

@router.delete("/{payment_id}")
async def delete_payment(payment_id: str):
    result = await db["payments"].delete_one({"paymentId": payment_id})
    if result.deleted_count == 1:
        return {"message": "Payment deleted"}
    raise HTTPException(status_code=404, detail="Payment not found")
