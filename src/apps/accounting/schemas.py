from pydantic import BaseModel


class SAccountRead(BaseModel):
    id: int
    balance: int

    model_config = {
        "from_attributes": True
    }


class STransactionRead(BaseModel):
    id: int
    amount: int

    model_config = {
        "from_attributes": True
    }
