from typing import Optional
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from starlette.responses import JSONResponse

from core.config import settings

class JwtService:

    Oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/signin")

    @staticmethod
    def  create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
        return encoded_jwt


    @staticmethod
    def create_response_with_jwt(user_id: int) -> JSONResponse:

        access_token = JwtService.create_access_token(
            data={"sub": user_id},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )

        response = JSONResponse(
            content={"status": "success", "access_token": access_token}
        )

        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=30 * 60,  # Срок действия куки (в секундах)
            secure=False,  # Только для HTTPS
            samesite="lax"
        )

        return response