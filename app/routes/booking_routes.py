from fastapi import APIRouter, HTTPException
from typing import List
from ..models.booking import Booking
from ..database import db
from ..utils.booking_utils import bookings_util

router = APIRouter()

@router.get("/bookings", response_model=List[Booking])
async def get_all_bookings():
    bookings_cursor = db["bookings"].find()
    bookings_list = []
    async for booking in bookings_cursor:
        bookings_list.append(bookings_util(booking))
    return bookings_list

@router.get("/bookings/{booking_id}", response_model=Booking)
async def get_booking(booking_id: str):
    booking = await db["bookings"].find_one({"bookingId": booking_id})
    if booking:
        return bookings_util(booking)
    raise HTTPException(status_code=404, detail="Booking not found")