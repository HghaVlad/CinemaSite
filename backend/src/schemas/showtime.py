from pydantic import BaseModel
from datetime import datetime
from typing import List


class Seat(BaseModel):
    row: int
    place: int

class ShowtimeResponse(BaseModel):
    id: int
    film_id: int
    datetime: datetime
    total_rows: int
    total_places_per_row: int
    booked_seats: List[Seat]

class ShowtimeListResponse(BaseModel):
    showtimes: List[ShowtimeResponse]
