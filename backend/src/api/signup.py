from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Coroutine

from db.postgres import get_postgres_session
from services.users import get_user_service

router = APIRouter(tags=["signup"])

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str

# TODO: Add JWT

@router.post("/signup")
async def submit_form(signup_data: SignUpRequest,
                      user_service_coroutine: Coroutine = Depends(get_user_service),
                      session: AsyncSession = Depends(get_postgres_session)
                      ):
    user_service = await user_service_coroutine
    user = await user_service.register_user(signup_data.email, signup_data.password, signup_data.name, signup_data.surname, session)
    return {"token": "future_JWT", "email": user.email, "name": user.name, "surname": user.surname}



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
#     <form action="/signup/submit" method="post">
#         <label for="email">Email:</label>
#         <input type="email" id="email" name="email"><br><br>
#         <label for="password">Password:</label>
#         <input type="text" id="password" name="password"><br><br>
#         <label for="name">Имя:</label>
#         <input type="text" id="name" name="name"><br><br>
#         <label for="surname">Фамилия:</label>
#         <input type="text" id="surname" name="surname"><br><br>
#         <input type="submit" value="Отправить">
#     </form>
# </body>
# </html>
# """
#
# @router.get("/signup", response_class=HTMLResponse)
# async def get_form():
#     return html_form
#
#
# @router.post("/signup/submit")
# async def submit_form(email: str = Form(...), password: str = Form(...),
#                       name: str = Form(...), surname: str = Form(...),
#                       user_service_coroutine: Coroutine = Depends(get_user_service),
#                       session: AsyncSession = Depends(get_postgres_session)
#                       ):
#     user_service = await user_service_coroutine
#     await user_service.add_user(email, password, name, surname, session)
#     return {"name": name, "email": email}


