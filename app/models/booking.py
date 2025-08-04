from pydantic import BaseModel
from datetime import datetime

class TimeSlot(BaseModel):
    startAt: datetime
    endAt: datetime


class Booking(BaseModel):
    bookingId: str
    customerId: str
    roomId: str
    bookingAt: datetime
    timeSlot: TimeSlot
    status: str
