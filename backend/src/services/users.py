from functools import lru_cache

from models.users import User
from db.postgres import get_postgres_session


# Example of user service
class UsersService:

    # In future there will be redis connection
    def __init__(self):
        pass

    async def get_user_by_id(self, user_id):
        async with get_postgres_session() as session:
            return await session.get(User, user_id)


@lru_cache
async def get_user_service() -> UsersService:
    return UsersService()