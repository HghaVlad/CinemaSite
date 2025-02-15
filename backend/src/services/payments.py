from functools import lru_cache
from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy import select


from db.postgres import AsyncSession
from models.showtime import Showtime, Ticket
from models.payments import Booking, Order, PaymentStatus
from schemas.Booking import MakeBooking
from schemas.Payment import UserPayment, OrderResponse
from utils import process_payment


class PaymentsService:

    @staticmethod
    async def book_showtime(booking: MakeBooking, session: AsyncSession, user_id, ) -> Ticket:
        showtime = await session.get(Showtime, booking.showtime_id)
        if not showtime:
            raise HTTPException(status_code=404, detail="Showtime not found")

        ticket = await session.get(Ticket, booking.ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        if ticket.is_booked:
            raise HTTPException(status_code=400, detail="Ticket is already booked")
        ticket.is_booked = True
        booking = Booking(ticket_id=ticket.id, user_id=user_id, price=showtime.price)

        ticket.bookings.append(booking)
        session.add(booking)
        session.add(ticket)
        await session.commit()

        return booking

    @staticmethod
    async def pay_showtime(payment: UserPayment, session: AsyncSession) -> PaymentStatus:

        booking = await session.get(Booking, payment.booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        status = process_payment(payment)
        booking.status = status
        # To do: make order file
        order = Order(user_id=booking.user_id, ticket_id=booking.ticket_id, payment_id=booking.id)

        session.add(order)
        await session.commit()

        return status

    @staticmethod
    async def get_user_orders(user_id, session: AsyncSession) -> List[OrderResponse]:
        orders = await session.execute(select(Order).where(Order.user_id == user_id))
        orders = orders.scalars().all()
        return [OrderResponse.from_orm(order) for order in orders]


@lru_cache
def get_payments_service() -> PaymentsService:
    return PaymentsService()
