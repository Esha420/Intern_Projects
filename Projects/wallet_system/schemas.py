from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    tier: Optional[str] = "Basic"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    balance: float

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    transaction_type: str
    amount: float
    details: str
    direction: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    transaction_id: str
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class SendMoney(BaseModel):
    recipient: str
    amount: float
    note: Optional[str] = None

class PayBill(BaseModel):
    bill_type: str
    account_number: str
    amount: float