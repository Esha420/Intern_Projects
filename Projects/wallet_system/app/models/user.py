from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    tier = Column(String)
    balance = Column(Float, default=0.0)

    sent_transactions = relationship("Transaction", back_populates="sender", foreign_keys='Transaction.sender_id')
    received_transactions = relationship("Transaction", back_populates="receiver", foreign_keys='Transaction.receiver_id')

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    amount = Column(Float)
    type = Column(String)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", back_populates="sent_transactions", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_transactions", foreign_keys=[receiver_id])
