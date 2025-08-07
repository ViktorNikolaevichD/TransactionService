from pydantic import BaseModel


class SAccountRead(BaseModel):
    id: int
    balance: int

    model_config = {
        "from_attributes": True
    }


class STransactionRead(BaseModel):
    id: str
    amount: int

    model_config = {
        "from_attributes": True
    }


class STransactionCreate(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: int
    signature: str
