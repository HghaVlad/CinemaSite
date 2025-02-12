from functools import lru_cache
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from starlette import status

from models.users import User
from db.postgres import get_postgres_session
from schemas.auth import SignUpRequest, SignInRequest


class UsersService:

    # In future there will be redis connection
    def __init__(self):
        self.PasswordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_id(self, user_id, session: AsyncSession):
        return await session.get(User, user_id)

    async def get_user_by_email(self, email: str, session: AsyncSession):
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def register_user(self, data: SignUpRequest, session: AsyncSession) -> User:
        if await self.get_user_by_email(data.email, session):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with such an email already exists",
            )

        hashed_password = self.PasswordContext.hash(data.password)
        user = User(email=data.email, hashed_password=hashed_password, name=data.name, surname=data.surname)
        session.add(user)
        await session.commit()
        await session.refresh(user)
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
            user = await self.get_user_by_id(user_id)
            await session.delete(user)
            await session.commit()


@lru_cache()
def get_user_service() -> UsersService:
    return UsersService()
