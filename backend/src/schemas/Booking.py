from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class MakeBooking(BaseModel):
    showtime_id: int
    row_number: int
    place_number: int


class BookingResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime
    price: Decimal

    class Config:
        from_attributes = True
