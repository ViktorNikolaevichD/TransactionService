from fastapi import FastAPI

from apps.auth.router import router as auth_router

app = FastAPI()
app.include_router(auth_router)


@app.get("")
async def docs():
    pass
