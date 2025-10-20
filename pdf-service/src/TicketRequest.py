from pydantic import BaseModel

class TicketRequest(BaseModel):
    film: str
    seat: str
    row: str
    time: str
    user_name: str
    user_surname: str
    user_email: str