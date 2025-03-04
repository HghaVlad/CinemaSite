from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from models.showtime import Showtime
from schemas.showtime import Seat, ShowtimeResponse

class ShowtimeService:

    # In future there will be redis connection
    def __init__(self):
        pass

    async def get_all_showtimes(self, session: AsyncSession) -> List[ShowtimeResponse]:
        query = (
            select(Showtime)
            .options(joinedload(Showtime.hall), joinedload(Showtime.tickets))
        )
        result = await session.execute(query)
        showtimes = result.scalars().all()

        print(1)
        # Формируем список ответов
        showtime_responses = []
        for showtime in showtimes:
            booked_seats = [
                Seat(row=ticket.row, place=ticket.place)
                for ticket in showtime.tickets
                if ticket.is_booked
            ]
            showtime_responses.append(
                ShowtimeResponse(
                    id=showtime.id,
                    film_id=showtime.film_id,
                    datetime=showtime.datetime,
                    total_rows=showtime.hall.rows,
                    total_places_per_row=showtime.hall.places,
                    booked_seats=booked_seats,
                )
            )

        return showtime_responses
    

    async def get_showtime_details(self, showtime_id: int, session: AsyncSession) -> Optional[ShowtimeResponse]:
        query = (
            select(Showtime)
            .options(joinedload(Showtime.hall), joinedload(Showtime.tickets))
            .where(Showtime.id == showtime_id)
        )
        result = await session.execute(query)
        showtime = result.scalars().first()

        if not showtime:
            return None

        # Формируем список занятых мест
        booked_seats = [
            Seat(row=ticket.row, place=ticket.place)
            for ticket in showtime.tickets
            if ticket.is_booked
        ]

        return ShowtimeResponse(
            id=showtime.id,
            film_id=showtime.film_id,
            datetime=showtime.datetime,
            total_rows=showtime.hall.rows,
            total_places_per_row=showtime.hall.places,
            booked_seats=booked_seats,
        )

@lru_cache
def get_showtime_service() -> ShowtimeService:
    return ShowtimeService()