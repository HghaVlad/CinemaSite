from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.films import Film


class FilmsService:

    # In future there will be redis connection
    def __init__(self):
        pass

    async def get_film_by_id(self, film_id, session: AsyncSession):
        return await session.get(Film, film_id)
    
    async def get_all_films(self, session: AsyncSession):
        result = await session.execute(select(Film))
        return result.scalars().all()
    

@lru_cache
def get_film_service() -> FilmsService:
    return FilmsService()