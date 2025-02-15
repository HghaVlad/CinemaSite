from fastapi import APIRouter, Depends
from typing import List

from services.payments import get_payments_service, PaymentsService
from models.payments import PaymentStatus, Booking
from schemas.Booking import MakeBooking
from schemas.Payment import UserPayment, OrderResponse


router = APIRouter(tags=["payments"])


@router.post("/book/", response_model=Booking)
async def book_showtime(ticket: MakeBooking, payments_service: PaymentsService = Depends(get_payments_service)):
    booking = await payments_service.book_showtime(ticket, user_id=1)

    return {"ticket": booking.json()}


@router.post("/pay/", response_model_include={"status": ["success", "failed", "not_enough_money"]})
async def pay_showtime(payment: UserPayment, payments_service: PaymentsService = Depends(get_payments_service)):
    status = await payments_service.pay_showtime(payment)
    if status == PaymentStatus.SUCCESS:
        return {"status": "success"}
    elif status == PaymentStatus.FAILED:
        return {"status": "failed"}
    elif status == PaymentStatus.NOT_ENOUGH_MONEY:
        return {"status": "not_enough_money"}

    return {"status": "error"}


@router.get("/orders/{user_id}", response_model=List[OrderResponse])
async def get_payment(user_id: int, payments_service: PaymentsService = Depends(get_payments_service)):
    return await payments_service.get_user_orders(user_id)

