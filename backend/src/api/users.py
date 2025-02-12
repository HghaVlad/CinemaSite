from fastapi import APIRouter, Depends

from services.users import get_user_service


router = APIRouter(tags=["users"])


# Example of user api
@router.get("/users/{user_id}")
async def get_user(user_id: int, user_service=Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    return {"user": user}

