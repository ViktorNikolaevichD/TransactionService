from fastapi import APIRouter, Depends

from apps.accounting.services import get_account_service
from apps.accounting.schemas import SAccountRead
from apps.user.models import User
from apps.user.utils import get_current_admin, get_current_user

router = APIRouter(
    prefix="/account",
    tags=["Счет"],
)


@router.get("/user/{user_id}", response_model=list[SAccountRead])
async def user_account(user_id: int, admin: User = Depends(get_current_admin)):
    return await get_account_service().get_accounts(user_id=user_id)


@router.get("/all", response_model=list[SAccountRead])
async def user_accounts(user: User = Depends(get_current_user)):
    return await get_account_service().get_accounts(user_id=user.id)
