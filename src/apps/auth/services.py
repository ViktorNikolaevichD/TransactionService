from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import HTTPException, status
from jose import jwt

from apps.user.models import User
from apps.user.services import get_user_service
from config import settings


class AuthService:
    async def auth_user(self, email: str, plain_password: str) -> Optional[str]:
        user: Optional[User] = await get_user_service().get_user(email=email)
        if not user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)
        if get_password_service().validate_password(plain_password, user.password):
            return await self.generate_jwt_token(
                data={
                    "user_id": user.id, 
                    "exp": datetime.now(tz=timezone) + timedelta(minutes=30),
                }
            )

    async def generate_jwt_token(data: dict[str, Any]) -> str:
        token = jwt.encode(
            claims=data,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALG,
        )
        return token


class PasswordService:
    @staticmethod
    def validate_password(plain_password: str, hashed_password: str) -> bool:
        ph = PasswordHasher()
        try:
            return ph.verify(hashed_password, plain_password)
        except VerificationError:
            return False


def get_auth_service() -> AuthService:
    return AuthService()


def get_password_service() -> PasswordService:
    return PasswordService()
