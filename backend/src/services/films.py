from functools import lru_cache
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from core.config import settings 
from models.films import Film
from schemas.films import FilmResponse, FilmListResponse, FilmCreate


class FilmsService:
    def __init__(self, redis: Redis):
        self.redis = redis


    async def get_film_by_id(self, film_id: int, session: AsyncSession) -> Optional[FilmResponse]:
        cache_key = f"film:{film_id}"
        cached_film = await self.redis.get(cache_key)

        if cached_film:
            return FilmResponse.parse_raw(cached_film)

        film = await session.get(Film, film_id)
        if film:
            film_response = FilmResponse.from_orm(film)
            await self.redis.set(cache_key, film_response.json(), ex=3600)  # ex=3600 время жизни кэша
            return film_response
        return None
    

    async def get_all_films(self, session: AsyncSession) -> FilmListResponse:
        cache_key = "films:all"
        cached_films = await self.redis.get(cache_key)

        if cached_films:
            return FilmListResponse.parse_raw(cached_films)

        result = await session.execute(select(Film))
        films = result.scalars().all()

        film_responses = [FilmResponse.from_orm(film) for film in films]
        film_list_response = FilmListResponse(films=film_responses)

        await self.redis.set(cache_key, film_list_response.json(), ex=3600)
        return film_list_response
    

    async def create_film(self, film: FilmCreate, session: AsyncSession) -> FilmResponse:
        new_film = Film(**film.dict())
        session.add(new_film)
        await session.commit()

        film_response = FilmResponse.from_orm(new_film)

        await self.redis.delete("films:all")
        return film_response


@lru_cache
def get_film_service() -> FilmsService:
    redis = Redis.from_url(settings.redis_config.redis_url, decode_responses=True)
    return FilmsService(redis)