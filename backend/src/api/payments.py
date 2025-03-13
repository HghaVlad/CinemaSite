from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict

from db.postgres import get_postgres_session, AsyncSession
from services.payments import get_payments_service, PaymentsService
from services.users import get_user_service, UsersService
from services.JwtService import JwtService
from models.payments import PaymentStatus
from schemas.booking import MakeBooking, BookingResponse
from schemas.payment import UserPayment, OrderResponse


router = APIRouter(tags=["payments"])


@router.post("/book/", response_model=BookingResponse)
async def book_showtime(ticket: MakeBooking,  payments_service: PaymentsService = Depends(get_payments_service),
                        session: AsyncSession = Depends(get_postgres_session),
                        user_service: UsersService = Depends(get_user_service),
                        credentials: HTTPAuthorizationCredentials = Security(JwtService.BearerScheme)):
    token = credentials.credentials
    user = await user_service.get_user_by_jwt(token, session)
    booking = await payments_service.book_showtime(ticket, session, user_id=user.id)

    return BookingResponse.model_validate(booking)


@router.post("/pay/", response_model_include={"status": ["success", "failed", "not_enough_money"], "url": str})
async def pay_showtime(
    payment: UserPayment,
    payments_service: PaymentsService = Depends(get_payments_service),
    session: AsyncSession = Depends(get_postgres_session)
) -> Dict[str, str]:
    status, ticket_url = await payments_service.pay_showtime(payment, session)

    if status == PaymentStatus.SUCCESS:
        return {"status": "success", "url": ticket_url}
    elif status == PaymentStatus.FAILED:
        return {"status": "failed", "url": ""}
    elif status == PaymentStatus.NOT_ENOUGH_MONEY:
        return {"status": "not_enough_money", "url": ""}

    return {"status": "error", "url": ""}


@router.get("/orders/", response_model=List[OrderResponse])
async def get_all_payment(payments_service: PaymentsService = Depends(get_payments_service),
                      session: AsyncSession = Depends(get_postgres_session),
                      user_service: UsersService = Depends(get_user_service),
                      credentials: HTTPAuthorizationCredentials = Security(JwtService.BearerScheme)):
    token = credentials.credentials
    user = await user_service.get_user_by_jwt(token, session)
    return await payments_service.get_user_orders(user.id, session)