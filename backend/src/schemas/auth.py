import re
from typing import Annotated
from pydantic import BaseModel, EmailStr, field_validator, AfterValidator


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    surname: str

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """
            Validates if a password is strong based on the following rules:
            - At least 8 characters long
            - Contains at least one uppercase letter
            - Contains at least one lowercase letter
            - Contains at least one digit
        """
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one digit.")
        print(value)
        return value

    @classmethod
    @field_validator("name", "surname")
    def validate_name(cls, value: str) -> str:
        """
        Checks if name and surname are valid
        """
        if value.isalpha() and len(value) >= 2:
            return value

        raise ValueError("Name should consist of 2 or more alphabetic characters")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str

    class Config:
        from_attributes = True


class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password", mode="after")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """
        The validator for the new_password field which is used from SignUpRequest.validate_password
        :param value: new password
        :return:
        """
        return SignUpRequest.validate_password(value)


class UpdateUserRequest(BaseModel):
    email: Annotated[EmailStr, None] = None
    name: Annotated[str, AfterValidator(SignUpRequest.validate_name), None] = None
    surname: Annotated[str, AfterValidator(SignUpRequest.validate_name), None] = None
