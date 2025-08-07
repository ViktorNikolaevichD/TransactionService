from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from apps.user.models import User
from apps.user.services import get_user_service
from config import settings

http_bearer = HTTPBearer(auto_error=True)


async def get_token(request: Request) -> str:
    credentials: Optional[HTTPAuthorizationCredentials] = await http_bearer(request=request)
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return credentials.credentials


async def get_valid_token(token: str = Depends(get_token)) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token=token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALG
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: Optional[str] = payload.get("exp")
    if not expire:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if expire_time <= datetime.now(tz=timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id: Optional[str] = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
                                    
    return payload


async def get_current_user(token: dict[str, Any] = Depends(get_valid_token)) -> User:
    user_id = token.get("user_id")
    user = await get_user_service().get_user(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
