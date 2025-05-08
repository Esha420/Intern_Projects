from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    tier: str

class UserLogin(BaseModel):
    username: str
    password: str

class TransactionCreate(BaseModel):
    receiver_username: Optional[str] = None
    amount: float
    type: str
    details: str

class TransactionOut(BaseModel):
    id: int
    sender_id: Optional[int]
    receiver_id: Optional[int]
    amount: float
    type: str
    details: str
    timestamp: datetime

    class Config:
        orm_mode = True
