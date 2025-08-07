from sqlalchemy import Sequence

from apps.accounting.models import Account
from apps.accounting.repositories import AccountRepository
from settings.services import BaseService


class AccountService(BaseService):
    async def get_accounts(self, **filter_by) -> Sequence[Account]:
        return await self.repository.find_all(**filter_by)


def get_account_service() -> AccountService:
    return AccountService(repo=AccountRepository)
