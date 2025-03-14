from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from db.postgres import get_postgres_session, AsyncSession

from services.showtime import ShowtimeService, get_showtime_service
from services.JwtService import JwtService
from services.users import get_user_service, UsersService
from schemas.showtime import ShowtimeResponse, ShowtimeListResponse, ShowtimeCreate, ShowTimeCreateResponse


router = APIRouter(tags=["showtimes"])


@router.get("/showtimes/{showtime_id}", response_model=ShowtimeResponse)
async def get_showtime_details(
    showtime_id: int,
    showtime_service: ShowtimeService = Depends(get_showtime_service),
    session: AsyncSession = Depends(get_postgres_session),
):
    showtime = await showtime_service.get_showtime_details(showtime_id, session)
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found")
    return showtime


@router.get("/showtimes", response_model=ShowtimeListResponse)
async def get_all_showtimes(
    showtime_service: ShowtimeService = Depends(get_showtime_service),
    session: AsyncSession = Depends(get_postgres_session),
):
    showtimes = await showtime_service.get_all_showtimes(session)
    if not showtimes:
        raise HTTPException(status_code=404, detail="No showtimes found")
    return ShowtimeListResponse(showtimes=showtimes)


@router.post("/showtime", response_model=ShowTimeCreateResponse)
async def create_showtime(showtime_data: ShowtimeCreate,
                          showtime_service: ShowtimeService = Depends(get_showtime_service),
                          session: AsyncSession = Depends(get_postgres_session),
                          user_service = Depends(get_user_service),
                          credentials: HTTPAuthorizationCredentials = Security(JwtService.BearerScheme)):

    token = credentials.credentials
    my_user = await user_service.get_user_by_jwt(token, session)
    if not my_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can get other users")
    new_showtime = await showtime_service.create_showtime(showtime_data, session)
    if new_showtime:
        return ShowTimeCreateResponse.model_validate(new_showtime)

    raise HTTPException(status_code=400, detail="Showtime already exists")