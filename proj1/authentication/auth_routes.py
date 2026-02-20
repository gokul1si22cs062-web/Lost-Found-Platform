from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from .auth_logic import db, hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserAuth(BaseModel):
    email: EmailStr
    password: str
    username: str = None # Optional for login

@router.post("/register")
async def register(user: UserAuth):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed = hash_password(user.password)
    await db.users.insert_one({
        "email": user.email, 
        "password": hashed, 
        "username": user.username
    })
    return {"message": "Success"}

@router.post("/login")
async def login(user: UserAuth):
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"user_id": str(db_user["_id"])})
    return {"access_token": token, "token_type": "bearer"}