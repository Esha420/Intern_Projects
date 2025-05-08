from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import user as schemas
from app.repository import wallet
from app.config.db import get_db
from app.services.auth import get_current_user
from typing import List


router = APIRouter()

@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return wallet.create_user(db, user)

@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return wallet.authenticate_user(db, user)

@router.post("/send")
def send_money(
    txn: schemas.TransactionCreate, 
    username: str, 
    db: Session = Depends(get_db)
):
    sender = get_current_user(username, db)
    return wallet.send_money(db, sender, txn.receiver_username, txn.amount, txn.details)

@router.post("/pay")
def pay_bill(
    txn: schemas.TransactionCreate, 
    username: str, 
    db: Session = Depends(get_db)
):
    user = get_current_user(username, db)
    return wallet.pay_bill(db, user, txn.amount, txn.details)

@router.get("/history", response_model=List[schemas.TransactionOut])
def history(username: str, db: Session = Depends(get_db)):
    user = get_current_user(username, db)
    return wallet.get_transactions(db, user)
