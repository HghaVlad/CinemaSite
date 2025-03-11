import requests
from fastapi.exceptions import HTTPException

from db.postgres import get_postgres_session
from core.config import settings
from models.payments import Booking
from models.users import User
from models.showtime import Ticket, Showtime
from models.films import Film


async def get_postgres_session_ticket_url(booking: Booking) -> str:

    url = f"{settings.pdf_api_host}/generate_pdf"

    session = await get_postgres_session()
    ticket = await session.get(Ticket, booking.ticket_id)
    user = await session.get(User, booking.user_id)
    showtime = await session.get(Showtime, ticket.showtime_id)
    film = await session.get(Film, showtime.film_id)

    data = {
        "film": film.name,
        "seat": ticket.place,
        "row": ticket.row,
        "time": showtime.datetime,
        "user_name": user.name,
        "user_surname": user.surname,
        "user_email": user.email
    }

    headers = {
        "pdf_api_token": settings.pdf_api_token
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return settings.pdf_api_host + response.content
    raise HTTPException(response.status_code, response.content)