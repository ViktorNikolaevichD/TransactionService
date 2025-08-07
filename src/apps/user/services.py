from typing import Optional

from apps.user.models import User
from apps.user.repositories import UserRepository
from settings.services import BaseService


class UserService(BaseService):
    async def get_user(self, **filter_by) -> Optional[User]:
        return await self.repository.find_one(**filter_by)


def get_user_service() -> UserService:
    return UserService(repo=UserRepository)
