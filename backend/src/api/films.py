from fastapi import APIRouter, Depends, HTTPException

from services.films import get_film_service, FilmsService
from schemas.films import FilmResponse, FilmListResponse
from db.postgres import get_postgres_session, AsyncSession

router = APIRouter(tags=["films"])


@router.get("/films/{film_id}", response_model=FilmResponse)
async def get_film(film_id: int, film_service=Depends(get_film_service),
                   session: AsyncSession = Depends(get_postgres_session)):
    film = await film_service.get_film_by_id(film_id, session)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return FilmResponse.model_validate(film)


@router.get("/films", response_model=FilmListResponse)
async def get_films_list(film_service: FilmsService = Depends(get_film_service),
                   session: AsyncSession = Depends(get_postgres_session)):
    film_list = await film_service.get_all_films(session)
    if not film_list:
        raise HTTPException(status_code=404, detail="Films not found")
    return FilmListResponse.model_validate(film_list)

