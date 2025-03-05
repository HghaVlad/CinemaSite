from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from models.films import Film
from schemas.films import FilmCreate


class FilmsService:

    # In future there will be redis connection
    def __init__(self):
        pass

    async def get_film_by_id(self, film_id, session: AsyncSession):
        return await session.get(Film, film_id)
    
    async def get_all_films(self, session: AsyncSession):
        result = await session.execute(select(Film))
        return result.scalars().all()

    async def create_film(self, film: FilmCreate, session: AsyncSession):
        new_film = Film(**film.dict())
        session.add(new_film)
        await session.commit()
        return new_film


@lru_cache
def get_film_service() -> FilmsService:
    return FilmsService()