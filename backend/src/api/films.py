from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials

from services.films import get_film_service, FilmsService
from services.JwtService import JwtService
from services.users import get_user_service
from schemas.films import FilmResponse, FilmListResponse, FilmCreate
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


@router.post("/films", response_model=FilmResponse)
async def create_film(film_data: FilmCreate, film_service: FilmsService = Depends(get_film_service),
                      session: AsyncSession = Depends(get_postgres_session),
                      credentials: HTTPAuthorizationCredentials = Security(JwtService.BearerScheme),
                      user_service = Depends(get_user_service)):

    token = credentials.credentials
    my_user = await user_service.get_user_by_jwt(token, session)
    if not my_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can get other users")

    new_film = await film_service.create_film(film_data, session)
    if new_film:
        return FilmResponse.model_validate(new_film)

    raise HTTPException(status_code=400, detail="Film already exists")