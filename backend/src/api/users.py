from fastapi import APIRouter, Depends, Request, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials

from services.JwtService import JwtService
from services.users import get_user_service, UsersService
from schemas.auth import UserResponse, UpdatePasswordRequest, UpdateUserRequest
from db.postgres import get_postgres_session, AsyncSession

router = APIRouter(tags=["users"])


# Example of user api
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service=Depends(get_user_service),
                   session: AsyncSession = Depends(get_postgres_session)):

    user = await user_service.get_user_by_id(user_id, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(user)


@router.get("/me", response_model=UserResponse)
async def get_me_user(user_service=Depends(get_user_service),
                        credentials: HTTPAuthorizationCredentials = Security(JwtService.BearerScheme),
                      session: AsyncSession = Depends(get_postgres_session)):
    """
    Вместо кукисов, тырит токен из http запроса с заголовком Authorization: Bearer <token>
    # по схеме из httpBearer
    """

    # user = await user_service.get_user_by_cookie_request(request, session)

    token = credentials.credentials
    user = await user_service.get_user_by_jwt(token, session)

    return UserResponse.from_orm(user)


@router.patch("/me", response_model=UserResponse)
async def update_me_user(request: Request, data: UpdateUserRequest,
                         credentials: HTTPAuthorizationCredentials = Security(JwtService.BearerScheme),
                         user_service: UsersService = Depends(get_user_service),
                         session: AsyncSession = Depends(get_postgres_session)):
    """
    Updates user's email, name, surname
    Request is expected to have "reset_password" field and if it exists and is true,
    new password will be generated and sent to new email
    Possible issue: entered email is not valid but password is changed and user never gets it
    Possible solution: have an url in email to confirm the changes (e.g. by asking to sing up with new data)
    """

    token = credentials.credentials
    old_user = await user_service.get_user_by_jwt(token, session)
    user = await user_service.update_user_data(old_user, request, data, session)

    return UserResponse.from_orm(user)


@router.post("/change_password")
async def change_password(request: Request, data: UpdatePasswordRequest,
                          credentials: HTTPAuthorizationCredentials = Security(JwtService.BearerScheme),
                          user_service: UsersService =Depends(get_user_service),
                          session: AsyncSession = Depends(get_postgres_session)):

    token = credentials.credentials
    old_user = await user_service.get_user_by_jwt(token, session)
    user = await user_service.change_password(old_user, request, data, session)

    return UserResponse.from_orm(user)