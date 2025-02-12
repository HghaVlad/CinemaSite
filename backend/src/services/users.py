from async_lru import alru_cache
from fastapi import HTTPException
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext
from starlette import status

from models.users import User
from db.postgres import get_postgres_session


# Example of user service
class UsersService:

    # In future there will be redis connection
    def __init__(self):
        self.PasswordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


    async def get_user_by_id(self, user_id):
        async with get_postgres_session() as session:
            return await session.get(User, user_id)


    async def register_user(self, email: str, password: str, name: str, surname: str, session: AsyncSession):
        hashed_password = self.PasswordContext.hash(password)
        user = User(email=email, hashed_password=hashed_password, name=name, surname=surname)
        session.add(user)
        await session.commit()
        await session.refresh(user)


    async def authenticate_user(self, email: str, password: str, session: AsyncSession):
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with such an email was not found",
            )
        if not self.PasswordContext.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password or email",
            )
        return user

    # Not working
    async def remove_user(self, user_id: int, session: AsyncSession):
        user = self.get_user_by_id(user_id)
        await session.delete(user)
        await session.commit()



@alru_cache
async def get_user_service() -> UsersService:
    return UsersService()