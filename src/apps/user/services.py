from typing import Optional

from sqlalchemy import Sequence

from apps.user.models import User
from apps.user.repositories import UserRepository
from settings.services import BaseService


class UserService(BaseService):
    async def get_user(self, **filter_by) -> Optional[User]:
        return await self.repository.find_one(**filter_by)

    async def get_users(self, **filter_by) -> Sequence[User]:
        return await self.repository.find_all(**filter_by)


def get_user_service() -> UserService:
    return UserService(repo=UserRepository)
