from fastapi import APIRouter, Depends, HTTPException
from db.postgres import get_postgres_session, AsyncSession

from services.showtime import ShowtimeService, get_showtime_service
from schemas.showtime import ShowtimeResponse, ShowtimeListResponse


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