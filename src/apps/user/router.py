from fastapi import APIRouter, Depends

from apps.user.models import User
from apps.user.services import get_user_service
from apps.user.schemas import SUserRead
from apps.user.utils import get_current_admin, get_current_user

router = APIRouter(
    prefix="/user",
    tags=["Пользователь"],
)


@router.get("/me", response_model=SUserRead)
async def login(user: User = Depends(get_current_user)):
    return user


@router.get("/all", response_model=list[SUserRead])
async def get_users(admin: User = Depends(get_current_admin)):
    users = await get_user_service().get_users(is_admin=False)
    return list(users)
