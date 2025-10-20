from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from services.users import get_user_service, UsersService
from services.JwtService import JwtService
from schemas.auth import SignInRequest, SignUpRequest
from db.postgres import get_postgres_session, AsyncSession

router = APIRouter(tags=["auth"])


@router.post("/signin")
async def signin(signin_data: SignInRequest, user_service: UsersService = Depends(get_user_service),
                 session: AsyncSession = Depends(get_postgres_session)):
    user_id = await user_service.authenticate_user(signin_data, session)
    response = JwtService.create_response_with_jwt(user_id)

    return response


@router.post("/signup")
async def signup(signup_data: SignUpRequest, user_service: UsersService = Depends(get_user_service),
                 session: AsyncSession = Depends(get_postgres_session)):
    user = await user_service.register_user(signup_data, session)
    response = JwtService.create_response_with_jwt(user.id)

    return response


@router.post("/logout")
async def logout():
    response = JSONResponse(status_code=200, content={"status": "success"})
    response.delete_cookie(key="user_id")
    return response
