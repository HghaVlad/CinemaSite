from pydantic import BaseModel
from datetime import datetime
from typing import List
from decimal import Decimal


class Seat(BaseModel):
    row: int
    place: int


class ShowtimeResponse(BaseModel):
    id: int
    film_id: int
    datetime: datetime
    total_rows: int
    total_places_per_row: int
    price: Decimal
    booked_seats: List[Seat]


class ShowtimeListResponse(BaseModel):
    showtimes: List[ShowtimeResponse]


class ShowtimeCreate(BaseModel):
    film_id: int
    datetime: datetime
    total_tickets: int
    rows: int
    places: int
    price: Decimal


class ShowTimeCreateResponse(BaseModel):
    id: int
    film_id: int
    datetime: datetime
    rows: int
    places: int
    price: Decimal

    class Config:
        from_attributes = True