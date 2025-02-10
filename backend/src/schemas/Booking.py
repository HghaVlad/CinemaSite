from pydantic import BaseModel


class MakeBooking(BaseModel):
    showtime_id: int
    seat_number: int
