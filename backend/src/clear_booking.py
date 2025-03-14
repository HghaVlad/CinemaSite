from asyncio import sleep

from datetime import datetime, timedelta
from sqlalchemy import select, delete, and_
from db.postgres import get_postgres_session
from models.payments import Booking, Payment, PaymentStatus
from models.showtime import Ticket


TIME_TO_DELETE: int = 300


async def clear():
    while True:
        try:
            async for session in get_postgres_session():
                stmt = (
                    select(Payment.booking_id)
                    .where(Payment.status == PaymentStatus.SUCCESS)
                )
                result = await session.execute(stmt)
                successed_payments = result.scalars().all()

                smt = (
                    select(Booking.id)
                    .where(and_(Booking.created_at < datetime.now() - timedelta(seconds=TIME_TO_DELETE),
                                Booking.created_at > datetime.now() - timedelta(seconds=TIME_TO_DELETE * 5)))
                )

                result = await session.execute(smt)
                all_bookings = result.scalars().all()

                failed_payments = [booking for booking in all_bookings if booking not in successed_payments]

                if failed_payments:
                    stmt = delete(Ticket).where(Ticket.id.in_(failed_payments))
                    await session.execute(stmt)
                    stmt = delete(Booking).where(Booking.id.in_(failed_payments))
                    await session.execute(stmt)
                    await session.commit()

            await sleep(TIME_TO_DELETE)

        except Exception as e:
            print(e)
            await sleep(5)