from fastapi import APIRouter, Depends, Request, HTTPException

from services.users import get_user_service
from schemas.auth import UserResponse
from db.postgres import get_postgres_session, AsyncSession

router = APIRouter(tags=["users"])


# Example of user api
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service=Depends(get_user_service),
                   session: AsyncSession = Depends(get_postgres_session)):
    user = await user_service.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(user)


@router.get("/me", response_model=UserResponse)
async def get_me_user(request: Request, user_service=Depends(get_user_service),
                      session: AsyncSession = Depends(get_postgres_session)):
    if request.cookies.get("user_id") and request.cookies.get("user_id").isdigit():
        user_id = int(request.cookies.get("user_id"))
        user = await user_service.get_user_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.from_orm(user)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

