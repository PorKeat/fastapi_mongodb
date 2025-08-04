from fastapi import APIRouter, HTTPException
from typing import List
from ..models.booking import Booking
from ..database import db

router = APIRouter()

@router.get("/", response_model=List[Booking])
async def get_all_bookings():
    cursor = db["bookings"].find()
    return [Booking(**doc) async for doc in cursor]

@router.get("/{booking_id}", response_model=Booking)
async def get_booking(booking_id: str):
    booking = await db["bookings"].find_one({"bookingId": booking_id})
    if booking:
        return Booking(**booking)
    raise HTTPException(status_code=404, detail="Booking not found")

@router.post("/", response_model=Booking)
async def create_booking(booking: Booking):
    result = await db["bookings"].insert_one(booking.dict())
    if result.inserted_id:
        return booking
    raise HTTPException(status_code=500, detail="Failed to create booking")

@router.put("/{booking_id}", response_model=Booking)
async def update_booking(booking_id: str, booking: Booking):
    result = await db["bookings"].replace_one({"bookingId": booking_id}, booking.dict())
    if result.modified_count == 1:
        return booking
    raise HTTPException(status_code=404, detail="Booking not found or not modified")

@router.delete("/{booking_id}")
async def delete_booking(booking_id: str):
    result = await db["bookings"].delete_one({"bookingId": booking_id})
    if result.deleted_count == 1:
        return {"message": "Booking deleted"}
    raise HTTPException(status_code=404, detail="Booking not found")
