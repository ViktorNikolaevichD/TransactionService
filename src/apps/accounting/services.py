from typing import Optional
from sqlalchemy import Sequence

from apps.accounting.models import Account, Transaction
from apps.accounting.repositories import AccountRepository, TransactionRepository
from settings.services import BaseService


class AccountService(BaseService):
    async def get_account(self, **filter_by) -> Optional[Account]:
        return await self.repository.find_one(**filter_by)
    
    async def get_accounts(self, **filter_by) -> Sequence[Account]:
        return await self.repository.find_all(**filter_by)


class TransactionService(BaseService):
    async def get_transactions(self, **filter_by) -> Sequence[Transaction]:
        return await self.repository.find_all(**filter_by)


def get_account_service() -> AccountService:
    return AccountService(repo=AccountRepository)


def get_transaction_service() -> TransactionService:
    return TransactionService(repo=TransactionRepository)
