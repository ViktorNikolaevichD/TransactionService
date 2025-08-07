from pydantic import BaseModel


class SUserRead(BaseModel):
    id: int
    email: str
    full_name: str

    model_config = {
        "from_attributes": True
    }
