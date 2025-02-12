from pydantic import BaseModel, EmailStr

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Coroutine

from db.postgres import get_postgres_session
from services.users import get_user_service

router = APIRouter(tags=["signin"])

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

# TODO: Add JWT

@router.post("/signin")
async def submit_form(signin_data: SignInRequest,
                      user_service_coroutine: Coroutine = Depends(get_user_service),
                      session: AsyncSession = Depends(get_postgres_session)
                      ):
    user_service = await user_service_coroutine
    user = await user_service.authenticate_user(signin_data.email, signin_data.password, session)
    return {"token": "future_JWT", "email": user.email, "name": user.name, "surname": user.surname}


# Old version via html form

# html_form = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Simple Form</title>
# </head>
# <body>
#     <h1>Введите данные</h1>
#     <form action="/signin/submit" method="post">
#         <label for="email">Email:</label>
#         <input type="email" id="email" name="email"><br><br>
#         <label for="password">Password:</label>
#         <input type="text" id="password" name="password"><br><br>
#         <input type="submit" value="Отправить">
#     </form>
# </body>
# </html>
# """

# @router.get("/signin", response_class=HTMLResponse)
# async def get_form():
#     return html_form

# @router.post("/signin/submit")
# async def submit_form(email: str = Form(...), password: str = Form(...),
#                       user_service_coroutine: Coroutine = Depends(get_user_service),
#                       session: AsyncSession = Depends(get_postgres_session)
#                       ):
#     user_service = await user_service_coroutine
#     res = await user_service.authorize_user(email, password, session)
#     if res:
#         return {"email": email}
#     return {"nonoo": "nonon"}