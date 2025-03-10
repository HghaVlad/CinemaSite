from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from models.showtime import Showtime
from schemas.showtime import Seat, ShowtimeResponse, ShowtimeCreate


class ShowtimeService:
    def __init__(self):
        pass


    async def get_showtime_details(self, showtime_id: int, session: AsyncSession) -> Optional[ShowtimeResponse]:
        query = (
            select(Showtime)
            .options(joinedload(Showtime.tickets))
            .where(Showtime.id == showtime_id)
        )
        result = await session.execute(query)
        showtime = result.scalars().first()

        if not showtime:
            return None

        booked_seats = [
            Seat(row=ticket.row, place=ticket.place)
            for ticket in showtime.tickets
        ]

        # Формируем ответ
        return ShowtimeResponse(
            id=showtime.id,
            film_id=showtime.film_id,
            datetime=showtime.datetime,
            total_rows=showtime.rows,
            total_places_per_row=showtime.places,
            price=showtime.price,
            booked_seats=booked_seats,
        )
    

    async def get_all_showtimes(self, session: AsyncSession) -> List[ShowtimeResponse]:
        query = (
            select(Showtime)
            .options(joinedload(Showtime.tickets))
        )
        result = await session.execute(query)
        showtimes = result.unique().scalars().all()

        # Формируем список ответов
        showtime_responses = []
        for showtime in showtimes:
            booked_seats = [
                Seat(row=ticket.row, place=ticket.place)
                for ticket in showtime.tickets
            ]
            showtime_responses.append(
                ShowtimeResponse(
                    id=showtime.id,
                    film_id=showtime.film_id,
                    datetime=showtime.datetime,
                    total_rows=showtime.rows,
                    total_places_per_row=showtime.places,
                    price=showtime.price,
                    booked_seats=booked_seats,
                )
            )

        return showtime_responses

    async def create_showtime(self, showtime_data: ShowtimeCreate, session: AsyncSession) -> Optional[ShowtimeResponse]:
        new_showtime = Showtime(
            film_id=showtime_data.film_id,
            datetime=showtime_data.datetime.replace(tzinfo=None),
            total_tickets=showtime_data.total_tickets,
            rows=showtime_data.rows,
            places=showtime_data.places)

        session.add(new_showtime)
        await session.commit()
        return new_showtime


@lru_cache
def get_showtime_service() -> ShowtimeService:
    return ShowtimeService()