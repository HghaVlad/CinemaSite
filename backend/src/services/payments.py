from functools import lru_cache
from typing import List, Tuple
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from db.postgres import AsyncSession
from models.films import Film
from models.showtime import Showtime, Ticket
from models.payments import Booking, Order, PaymentStatus, Payment
from schemas.booking import MakeBooking
from schemas.payment import UserPayment, OrderResponse, TicketResponse, ShowtimeResponseWithFilm
from schemas.films import FilmResponse
from utils import process_payment
from pdf_integration import get_ticket_url


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
    async def pay_showtime(payment: UserPayment, session: AsyncSession) -> Tuple[PaymentStatus, str]:

        booking = await session.get(Booking, payment.booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        status = process_payment(payment)
        booking.status = status

        new_payment = Payment(booking_id=booking.id, card_number=payment.card_number, card_holder=payment.card_holder, cvv=payment.cvv, status=status)
        session.add(new_payment)
        await session.commit()
        
        ticket_url = ""
        if status == PaymentStatus.SUCCESS:
            ticket_url = await get_ticket_url(booking=booking)

            order = Order(user_id=booking.user_id, ticket_id=booking.ticket_id, payment_id=new_payment.id, ticket_url=ticket_url)
            session.add(order)
            await session.commit()
        else:
            ticket = await session.get(Ticket, booking.ticket_id)
            await session.delete(ticket)
            await session.delete(booking)
            await session.commit()

        await session.refresh(booking)

            
        return (status, ticket_url)

    @staticmethod
    async def get_user_orders(user_id: int, session: AsyncSession) -> List[OrderResponse]:
        # Загружаем заказы и связанные билеты с помощью JOIN
        stmt = (
            select(Order, Ticket, Showtime, Film)
            .join(Ticket, Order.ticket_id == Ticket.id)
            .join(Showtime, Ticket.showtime_id == Showtime.id)
            .join(Film, Showtime.film_id == Film.id)
            .where(Order.user_id == user_id)
        )
        result = await session.execute(stmt)
        orders_with_tickets = result.all()

        order_responses = []
        for order, ticket, showtime, film in orders_with_tickets:
            ticket_response = TicketResponse.from_orm(ticket)
            print(order)
            showtime = ShowtimeResponseWithFilm.from_orm(showtime)
            showtime.film = FilmResponse.from_orm(film)
            order_response = OrderResponse(
                id=order.id,
                user_id=order.user_id,
                ticket=ticket_response,
                payment_id=order.payment_id,
                created_at=order.created_at.isoformat(),
                ticket_url=order.ticket_url,
                showtime = showtime
            )
            order_responses.append(order_response)

        return order_responses


@lru_cache
def get_payments_service() -> PaymentsService:
    return PaymentsService()
