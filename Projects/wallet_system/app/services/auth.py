from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.config.db import get_db
from app.models.user import User

def get_current_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
