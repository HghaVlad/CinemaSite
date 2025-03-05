from typing import Optional

from pydantic import BaseModel, EmailStr


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

