from pydantic import BaseModel


class UserPayment(BaseModel):
    booking_id: int
    card_number: str
    card_holder: str
    cvv: int


class TicketResponse(BaseModel):
    id: int
    showtime_id: int
    ticket_id: int
    created_at: str

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    payment_id: int
    ticket: TicketResponse

    created_at: str

    class Config:
        from_attributes = True

