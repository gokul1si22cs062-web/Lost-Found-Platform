from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from motor.motor_asyncio import AsyncIOMotorClient

# 1. Database Setup (Self-contained)
# Replace the URL with your Member 5's URL when they provide it
MONGO_URL = "mongodb://localhost:27017" 
client = AsyncIOMotorClient(MONGO_URL)
db = client.lost_and_found_db 

# 2. Security Setup
SECRET_KEY = "DEV_SECRET_KEY_99" 
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)