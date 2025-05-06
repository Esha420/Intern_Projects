from sqlalchemy.orm import Session
import models, schemas, crud
from passlib.context import CryptContext
import random
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        password=hashed_password,
        tier=user.tier
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    transaction_id = ''.join(random.choices('0123456789ABCDEF', k=8))
    db_transaction = models.Transaction(
        transaction_id=transaction_id,
        user_id=user_id,
        **transaction.dict()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id
    ).offset(skip).limit(limit).all()