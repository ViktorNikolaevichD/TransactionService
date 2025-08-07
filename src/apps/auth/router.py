from fastapi import APIRouter

from apps.auth.services import get_auth_service
from apps.auth.shemas import SLogin

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post("/sign-in")
async def login(login_cred: SLogin) -> str:
    return await get_auth_service().auth_user(
        email=login_cred.email, 
        plain_password=login_cred.password
    )
