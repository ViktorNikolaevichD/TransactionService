from pydantic import BaseModel, EmailStr


class SUserRead(BaseModel):
    id: int
    email: str
    full_name: str

    model_config = {
        "from_attributes": True
    }


class SUserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class SUserUpdate(SUserCreate):
    ...
