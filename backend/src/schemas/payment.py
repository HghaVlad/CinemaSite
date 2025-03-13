from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

from .showtime import ShowtimeResponseWithFilm

class UserPayment(BaseModel):
    booking_id: int
    card_number: str
    card_holder: str
    cvv: int


class TicketResponse(BaseModel):
    id: int
    showtime_id: int

    price: Decimal
    row: int
    place: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    ticket: TicketResponse
    payment_id: int

    created_at: str
    ticket_url: str

    showtime: Optional[ShowtimeResponseWithFilm]

    class Config:
        from_attributes = True

