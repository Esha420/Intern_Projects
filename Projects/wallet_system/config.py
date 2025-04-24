import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///wallet.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Transaction limits by tier (in base currency units)
    TRANSACTION_LIMITS = {
        'basic': {'daily': 1000, 'monthly': 10000},
        'premium': {'daily': 5000, 'monthly': 50000},
        'business': {'daily': 50000, 'monthly': 500000}
    }