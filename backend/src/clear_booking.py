from asyncio import sleep

from datetime import datetime, timedelta
from sqlalchemy import select, delete
from db.postgres import get_postgres_session
from models.payments import Booking
from models.showtime import Ticket


TIME_TO_DELETE: int = 300

async def clear():
    while True:
        async for session in get_postgres_session():
            stmt = (
                select(Booking)
                .where(datetime.now() - Booking.created_at >= timedelta(seconds=TIME_TO_DELETE))
            )
            result = await session.execute(stmt)
            expired_bookings = result.scalars().all()

            if expired_bookings:
                ticket_ids_to_delete = [booking.ticket_id for booking in expired_bookings]
                stmt = (
                    delete(Ticket)
                    .where(Ticket.id.in_(ticket_ids_to_delete))
                )
                await session.execute(stmt)

                stmt = (
                    delete(Booking)
                    .where(datetime.now() - Booking.created_at >= timedelta(seconds=TIME_TO_DELETE))
                )
                await session.execute(stmt)

                await session.commit()

        await sleep(TIME_TO_DELETE)