from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status

from apps.user.models import User
from apps.user.services import get_user_service
from apps.user.schemas import SUserRead, SUserCreate, SUserUpdate
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


@router.post("", response_model=SUserRead)
async def create_user(user_data: SUserCreate, admin: User = Depends(get_current_admin)):
    data = user_data.model_dump()
    try:
        return await get_user_service().create_user(data=data)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.put("/{user_id}", response_model=SUserRead)
async def update_user(user_id: int, user_data: SUserUpdate, admin: User = Depends(get_current_admin)):
    data = user_data.model_dump()
    try:
        return await get_user_service().update_user(data=data, id=user_id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete("/{user_id}")
async def delete_user(user_id: int, admin: User = Depends(get_current_admin)):
    await get_user_service().delete_user(id=user_id)
