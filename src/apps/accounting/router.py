from fastapi import APIRouter, Depends, HTTPException, status

from apps.accounting.services import get_account_service, get_transaction_service
from apps.accounting.schemas import SAccountRead, STransactionRead
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


@router.get("/{account_id}", response_model=list[STransactionRead])
async def get_account_transactions(account_id: int, user: User = Depends(get_current_user)):
    if user.is_admin:
        return await get_transaction_service().get_transactions(account_id=account_id)
    account = await get_account_service().get_account(id=account_id, user_id=user.id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await get_transaction_service().get_transactions(account_id=account_id)
