from fastapi import FastAPI

from apps.auth.router import router as auth_router
from apps.user.router import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)


@app.get("")
async def docs():
    pass
