from ..models import Transaction, User
from .. import db
from datetime import datetime, timedelta
from ..utils.security import generate_reference

class TransactionService:
    
    @staticmethod
    def create_transaction(user_id, amount, transaction_type, recipient_id=None, merchant_id=None):
        user = User.query.get(user_id)
        
        # Check balance for outgoing transactions
        if transaction_type in ['transfer', 'payment', 'withdrawal']:
            if user.balance < amount:
                raise ValueError("Insufficient balance")
        
        # Calculate fee based on user tier
        fee_percentage = 1.5  # Default fee (would normally come from config)
        fee = amount * (fee_percentage / 100)
        
        # Create transaction
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            recipient_id=recipient_id,
            merchant_id=merchant_id,
            fee=fee,
            reference=generate_reference(),
            status='pending'
        )
        
        db.session.add(transaction)
        db.session.commit()
        return transaction