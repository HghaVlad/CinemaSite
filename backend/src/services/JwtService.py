from typing import Optional
from datetime import datetime, timedelta

from fastapi.security import HTTPBearer
from jose import jwt
from starlette.responses import JSONResponse
from core.config import settings


class JwtService:
    BearerScheme = HTTPBearer()

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=10000))  # 10000 - по воле Влада Йошигаке
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def create_response_with_jwt(user_id: int) -> JSONResponse:
        access_token = JwtService.create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )

        response: JSONResponse = JSONResponse(
            content={"status": "success",
                     "access_token": access_token,
                     "token_type": "bearer"}
        )

        # Просто возращается, без кук, по приказу господина Кайзена-Бухарина
        return response
