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
    
    async def create_user(self, data: dict) -> User:
        data = data.copy()
        from apps.auth.services import get_password_service
        data["password"] = get_password_service().hash_password(data["password"])
        return await self.repository.add_one(data=data)

    async def update_user(self, data: dict, **filter_by) -> Optional[User]:
        data = data.copy()
        from apps.auth.services import get_password_service
        data["password"] = get_password_service().hash_password(data["password"])
        return await self.repository.update_one(data=data, **filter_by)

    async def delete_user(self, **filter_by) -> None:
        return await self.repository.delete_one(**filter_by)


def get_user_service() -> UserService:
    return UserService(repo=UserRepository)
