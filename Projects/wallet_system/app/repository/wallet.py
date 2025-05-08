from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models import user as models
from app.schemas import user as schemas


TIER_BALANCE = {
    "Gold": 1000,
    "Platinum": 5000,
    "Diamond": 10000
}

TIER_LIMIT = {
    "Gold": 500,
    "Platinum": 2000,
    "Diamond": float("inf")
}

def create_user(db: Session, user: schemas.UserCreate):
    if user.tier not in TIER_BALANCE:
        raise HTTPException(status_code=400, detail="Invalid tier")

    db_user = models.User(
        username=user.username,
        password=user.password,
        tier=user.tier,
        balance=TIER_BALANCE[user.tier]
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")

    return db_user

def authenticate_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).filter_by(username=user.username, password=user.password).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_user

def send_money(db: Session, sender: models.User, receiver_username: str, amount: float, note: str):
    receiver = db.query(models.User).filter_by(username=receiver_username).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    limit = TIER_LIMIT[sender.tier]
    if amount > limit:
        raise HTTPException(status_code=403, detail=f"Transaction limit exceeded for {sender.tier} tier")

    sender.balance -= amount
    receiver.balance += amount

    transaction = models.Transaction(
        sender=sender,
        receiver=receiver,
        amount=amount,
        type="Send Money",
        details=note
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction

def pay_bill(db: Session, user: models.User, amount: float, details: str):
    if user.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    user.balance -= amount

    transaction = models.Transaction(
        sender=user,
        receiver=None,
        amount=amount,
        type="Pay Bill",
        details=details
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction

def get_transactions(db: Session, user: models.User):
    return db.query(models.Transaction).filter(
        (models.Transaction.sender_id == user.id) | 
        (models.Transaction.receiver_id == user.id)
    ).order_by(models.Transaction.timestamp.desc()).all()
