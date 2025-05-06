from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import random

import models, crud, schemas
from schemas import UserCreate, SendMoney, PayBill
from database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Security
SECRET_KEY = "your-secret-key"
ALGORCHEMY = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db, username: str, password: str):
    user = crud.get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORCHEMY)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORCHEMY])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user

@app.post("/send_money/")
async def send_money(
    send_data: SendMoney,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check recipient exists
    recipient = crud.get_user(db, username=send_data.recipient)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    # Check sufficient balance
    if send_data.amount > current_user.balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Check tier limits
    if current_user.tier == "Basic" and send_data.amount > 500:
        raise HTTPException(status_code=400, detail="Basic tier limit: $500 per transaction")
    elif current_user.tier == "Premium" and send_data.amount > 2000:
        raise HTTPException(status_code=400, detail="Premium tier limit: $2000 per transaction")
    
    # Update balances
    current_user.balance -= send_data.amount
    recipient.balance += send_data.amount
    
    # Create transactions
    transaction_id = ''.join(random.choices('0123456789ABCDEF', k=8))
    timestamp = datetime.utcnow()
    
    # Sender's transaction
    sender_transaction = schemas.TransactionCreate(
        transaction_type="send_money",
        amount=send_data.amount,
        details=f"To: {send_data.recipient}, Note: {send_data.note}",
        direction="out"
    )
    crud.create_transaction(db, sender_transaction, current_user.id)
    
    # Recipient's transaction
    recipient_transaction = schemas.TransactionCreate(
        transaction_type="receive_money",
        amount=send_data.amount,
        details=f"From: {current_user.username}, Note: {send_data.note}",
        direction="in"
    )
    crud.create_transaction(db, recipient_transaction, recipient.id)
    
    db.commit()
    
    return {
        "message": "Transaction successful",
        "transaction_id": transaction_id,
        "new_balance": current_user.balance
    }

@app.post("/pay_bill/")
async def pay_bill(
    bill_data: PayBill,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check sufficient balance
    if bill_data.amount > current_user.balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Update balance
    current_user.balance -= bill_data.amount
    
    # Create transaction
    transaction_id = ''.join(random.choices('0123456789ABCDEF', k=8))
    
    transaction = schemas.TransactionCreate(
        transaction_type="pay_bill",
        amount=bill_data.amount,
        details=f"Bill: {bill_data.bill_type}, Account: {bill_data.account_number}",
        direction="out"
    )
    crud.create_transaction(db, transaction, current_user.id)
    
    db.commit()
    
    return {
        "message": "Bill payment successful",
        "transaction_id": transaction_id,
        "new_balance": current_user.balance
    }

@app.get("/transactions/", response_model=List[schemas.Transaction])
async def get_transactions(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_transactions(db, user_id=current_user.id)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Digital Wallet API",
        "endpoints": {
            "documentation": "/docs",
            "redoc": "/redoc",
            "login": "/token",
            "create_user": "/users/",
            "get_user": "/users/me/",
            "send_money": "/send_money/",
            "pay_bill": "/pay_bill/",
            "transactions": "/transactions/"
        }
    }