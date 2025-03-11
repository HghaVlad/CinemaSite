from functools import lru_cache
from fastapi.exceptions import HTTPException
from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from starlette import status
from jose import jwt, JWTError

from models.users import User
from db.postgres import get_postgres_session
from core.config import settings


from schemas.auth import SignUpRequest, SignInRequest, UpdatePasswordRequest, UpdateUserRequest
from utils import send_registration_email, generate_new_password, send_reset_password_email


class UsersService:

    def __init__(self):
        self.PasswordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_cookie_request(self, request: Request, session: AsyncSession):
        if request.cookies.get("user_id") and request.cookies.get("user_id").isdigit():
            user_id = int(request.cookies.get("user_id"))
            user = await self.get_user_by_id(user_id, session)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")


    async def get_user_by_id(self, user_id, session: AsyncSession):
        return await session.get(User, user_id)


    async def get_user_by_email(self, email: str, session: AsyncSession):
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()


    async def get_user_by_jwt(self, token: str, session: AsyncSession):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
            user_id: int = int(payload.get("sub"))
            if user_id is None:
                raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен истек",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except JWTError as e:
            print(e)
            raise credentials_exception

        user = await self.get_user_by_id(user_id, session)

        if user is None:
            raise credentials_exception

        return user


    async def register_user(self, data: SignUpRequest, session: AsyncSession) -> User:

        if await self.get_user_by_email(str(data.email), session):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with such an email already exists",
            )

        hashed_password = self.PasswordContext.hash(data.password)
        user = User(email=str(data.email), hashed_password=hashed_password, name=data.name, surname=data.surname)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        await send_registration_email(str(data.email), data.name)
        return user


    async def authenticate_user(self, data: SignInRequest, session: AsyncSession) -> int:
        result = await session.execute(select(User).where(User.email == data.email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with such an email was not found",
            )

        if not self.PasswordContext.verify(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password or email",
            )
        return user.id


    # Not working
    async def remove_user(self, user_id: int):
        async with get_postgres_session() as session:
            user = await self.get_user_by_id(user_id, session)
            await session.delete(user)
            await session.commit()


    async def update_user_data(self, user: User, request: Request, data: UpdateUserRequest, session: AsyncSession):
        """
        Updates user's email, name, surname if they are valid
        """
        print(data, "ey")
        if data.email is not None:
            user.email = data.email
        if data.name is not None:
            user.name = data.name
        if data.surname is not None:
            user.surname = data.surname

        session.add(user)
        await session.commit()
        return user


    async def change_password(self, user: User, request: Request, data: UpdatePasswordRequest, session: AsyncSession):

        if not self.PasswordContext.verify(data.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect old password",
            )
        user.hashed_password = self.PasswordContext.hash(data.new_password)
        session.add(user)
        await session.commit()
        return user


    async def reset_password(self, request: Request, session: AsyncSession):
        user = await self.get_user_by_cookie_request(request, session)
        new_password = generate_new_password()
        await send_reset_password_email(str(user.email), str(user.name), new_password)
        user.hashed_password = self.PasswordContext.hash(new_password)

        await session.commit()
        await session.refresh(user)
        return user



@lru_cache()
def get_user_service() -> UsersService:
    return UsersService()
