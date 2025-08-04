from fastapi import APIRouter, HTTPException
from typing import List
from ..models.payment import Payment
from ..database import db
from ..utils.payment_utils import payments_util

router = APIRouter()

@router.get("/payments", response_model=List[dict])
async def get_all_payments():
    payments_cursor = db["payments"].find()
    payments_list = []
    async for payment in payments_cursor:
        payments_list.append(payments_util(payment))
    return payments_list

@router.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(payment_id: str):
    payment = await db["payments"].find_one({"paymentId": payment_id})
    if payment:
        return payments_util(payment)
    raise HTTPException(status_code=404, detail="Payment not found")