import jwt
from datetime import datetime, timedelta
import random
import string
from ..config import Config

def generate_reference():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"TX{timestamp}{rand_str}"

def generate_jwt_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')