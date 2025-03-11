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
        # Проверяем, есть ли данные в кэше
        cache_key = f"film:{film_id}"
        cached_film = await self.redis.get(cache_key)

        if cached_film:
            # Если данные есть в кэше, десериализуем их в FilmResponse
            return FilmResponse.parse_raw(cached_film)

        # Если данных нет в кэше, запрашиваем их из базы данных
        film = await session.get(Film, film_id)
        if film:
            # Сериализуем объект Film в FilmResponse
            film_response = FilmResponse.from_orm(film)
            await self.redis.set(cache_key, film_response.json(), ex=3600)  # ex=3600 — TTL (время жизни кэша)
            return film_response
        return None
    

    async def get_all_films(self, session: AsyncSession) -> FilmListResponse:
        # Проверяем, есть ли данные в кэше
        cache_key = "films:all"
        cached_films = await self.redis.get(cache_key)

        if cached_films:
            # Если данные есть в кэше, десериализуем их в FilmListResponse
            return FilmListResponse.parse_raw(cached_films)

        # Если данных нет в кэше, запрашиваем их из базы данных
        result = await session.execute(select(Film))
        films = result.scalars().all()

        # Сериализуем объекты Film в список FilmResponse
        film_responses = [FilmResponse.from_orm(film) for film in films]
        film_list_response = FilmListResponse(films=film_responses)

        # Сохраняем данные в кэше
        await self.redis.set(cache_key, film_list_response.json(), ex=3600)
        return film_list_response
    

    async def create_film(self, film: FilmCreate, session: AsyncSession) -> FilmResponse:
        # Создаем новый объект Film из FilmCreate
        new_film = Film(**film.dict())
        session.add(new_film)
        await session.commit()

        # Сериализуем новый объект Film в FilmResponse
        film_response = FilmResponse.from_orm(new_film)

        # Инвалидируем кэш для списка всех фильмов
        await self.redis.delete("films:all")
        return film_response


@lru_cache
def get_film_service() -> FilmsService:
    # Создаем подключение к Redis, используя настройки из settings
    redis = Redis.from_url(settings.redis_config.redis_url, decode_responses=True)
    return FilmsService(redis)