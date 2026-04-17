import time
import jwt
import bcrypt

SECRET_KEY = "scholar-agent-secret-key"
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    # Truncate to 72 bytes natively to avoid any length limits
    truncated_pwd = password.encode('utf-8')[:72]
    return bcrypt.hashpw(truncated_pwd, bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = time.time() + 3600 # 1 hour
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
