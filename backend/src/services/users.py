import random
import re
import string
from functools import lru_cache
from fastapi.exceptions import HTTPException
from fastapi import Request
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
        self.EmailRegex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


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


    async def register_user(self, data: SignUpRequest, session: AsyncSession) -> User:

        if await self.get_user_by_email(str(data.email), session):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with such an email already exists",
            )

        # Checking if name and surname are correct, invalid email format should be caught by pydantic EmailStr
        name = data.name.strip()
        surname = data.surname.strip()
        self.is_name_or_surname_valid(name, "Name")
        self.is_name_or_surname_valid(surname, "Surname")

        # Checking if password is strong enough
        is_pwd_strong, pwd_msg = self.is_password_strong(data.password)
        if not is_pwd_strong:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=pwd_msg,
            )

        hashed_password = self.PasswordContext.hash(data.password)
        user = User(email=str(data.email), hashed_password=hashed_password, name=name, surname=surname)

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


    async def update_user_data(self, request: Request, session: AsyncSession):
        """
            Updates user's email, name, surname if they are valid
        """
        user = await self.get_user_by_cookie_request(request, session)

        if not request.cookies.get("email") or not request.cookies.get("name") or not request.cookies.get("surname"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Email or name or surname are missing in the http request cookies",
            )


        email = request.cookies.get("email").strip()
        if re.match(self.EmailRegex, email):
            user.email = email
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format",
            )

        name = request.cookies.get("name").strip()
        if self.is_name_or_surname_valid(name, "Name"):
            user.name = name

        surname = request.cookies.get("surname").strip()
        if self.is_name_or_surname_valid(name, "Surname"):
            user.surname = surname

        await session.commit()
        await session.refresh(user)
        return user


    def is_password_strong(self, password) -> (bool, str):
        """
        Validates if a password is strong based on the following rules:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        """
        # Minimum length
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        # At least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter."

        # At least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter."

        # At least one digit
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one digit."

        # If all checks pass
        return True, "Password is strong."


    def is_name_or_surname_valid(self, name: str, first_or_last: str) -> bool:
        if name.isalpha() and len(name) >= 2:
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{first_or_last} should consist of 2 or more alphabetic characters"
            )


    def generate_new_password(self):
        """
        Generates a random password that meets the following criteria:
        - 8-16 characters long.
        - Contains at least one lowercase letter.
        - Contains at least one uppercase letter.
        - Contains at least one digit.
        """

        length = random.randint(8, 16)

        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits

        # Ensure at least one character from each set
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
        ]

        # Fill the rest of the password with random choices from all sets
        all_characters = lowercase + uppercase + digits
        password += random.choices(all_characters, k=length - 3)

        # Shuffle the password to avoid predictable patterns
        random.shuffle(password)

        # Convert the list to a string
        return ''.join(password)


@lru_cache()
def get_user_service() -> UsersService:
    return UsersService()
