from functools import lru_cache
from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy import select


from db.postgres import AsyncSession
from models.showtime import Showtime, Ticket
from models.payments import Booking, Order, PaymentStatus, Payment
from schemas.Booking import MakeBooking
from schemas.Payment import UserPayment, OrderResponse
from utils import process_payment


class PaymentsService:

    @staticmethod
    async def book_showtime(booking: MakeBooking, session: AsyncSession, user_id, ) -> Ticket:
        showtime = await session.get(Showtime, booking.showtime_id)
        if not showtime:
            raise HTTPException(status_code=404, detail="Showtime not found")

        if showtime.rows < booking.row_number or booking.row_number < 1:
            raise HTTPException(status_code=400, detail="Row number is out of range")
        if showtime.places < booking.place_number or booking.place_number < 1:
            raise HTTPException(status_code=400, detail="Place number is out of range")

        result = await session.execute(
            select(Ticket).where(Ticket.showtime_id == showtime.id, Ticket.row == booking.row_number, Ticket.place == booking.place_number)
        )
        if result.scalar():
            raise HTTPException(status_code=400, detail="Ticket is already booked")

        ticket = Ticket(showtime_id=showtime.id, row=booking.row_number, place=booking.place_number, price=showtime.price)
        session.add(ticket)
        await session.commit()
        await session.refresh(ticket)
        booking = Booking(ticket_id=ticket.id, user_id=user_id, price=showtime.price)

        session.add(booking)
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
        new_payment = Payment(booking_id=booking.id, card_number=payment.card_number, card_holder=payment.card_holder, cvv=payment.cvv, status=status)
        session.add(new_payment)
        await session.commit()
        if status == PaymentStatus.SUCCESS:
            order = Order(user_id=booking.user_id, ticket_id=booking.ticket_id, payment_id=new_payment.id)

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
