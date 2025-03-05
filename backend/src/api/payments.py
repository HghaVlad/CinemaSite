from fastapi import APIRouter, Depends, Request
from typing import List

from db.postgres import get_postgres_session, AsyncSession
from services.payments import get_payments_service, PaymentsService
from services.users import get_user_service, UsersService
from models.payments import PaymentStatus, Booking
from schemas.Booking import MakeBooking, BookingResponse
from schemas.Payment import UserPayment, OrderResponse


router = APIRouter(tags=["payments"])


@router.post("/book/", response_model=BookingResponse)
async def book_showtime(ticket: MakeBooking, request: Request, payments_service: PaymentsService = Depends(get_payments_service),
                        session: AsyncSession = Depends(get_postgres_session),
                        user_service: UsersService = Depends(get_user_service)):
    user = await user_service.get_user_by_cookie_request(request, session)
    booking = await payments_service.book_showtime(ticket, session, user_id=user.id)

    return BookingResponse.model_validate(booking)


@router.post("/pay/", response_model_include={"status": ["success", "failed", "not_enough_money"]})
async def pay_showtime(payment: UserPayment, payments_service: PaymentsService = Depends(get_payments_service),
                       session: AsyncSession = Depends(get_postgres_session)):
    status = await payments_service.pay_showtime(payment, session)
    if status == PaymentStatus.SUCCESS:
        return {"status": "success"}
    elif status == PaymentStatus.FAILED:
        return {"status": "failed"}
    elif status == PaymentStatus.NOT_ENOUGH_MONEY:
        return {"status": "not_enough_money"}

    return {"status": "error"}


@router.get("/orders/{user_id}", response_model=List[OrderResponse])
async def get_payment(user_id: int, payments_service: PaymentsService = Depends(get_payments_service),
                      session: AsyncSession = Depends(get_postgres_session)):
    return await payments_service.get_user_orders(user_id, session)
