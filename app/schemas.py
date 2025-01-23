from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class TransactionCreate(BaseModel):
    transaction_type: str
    party_name: str
    description: str
    quantity: float
    total_value: float
    payment_detail: str
