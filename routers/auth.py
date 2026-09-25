from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import get_db
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "pasagadang-sultan-key-2026-ganti-di-render")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username itu isinya EMAIL lu bro!
    # contoh: admin@pasagadang.com
    
    # Query ke DB pasagadang.admins
    result = db.execute(text("SELECT * FROM admins WHERE email = :email AND is_active = 1"), {"email": form_data.username})
    admin = result.mappings().first()
    
    if not admin:
        raise HTTPException(status_code=400, detail="Email gak ketemu di DB pasagadang")
    
    if not verify_password(form_data.password, admin["password_hash"]):
        raise HTTPException(status_code=400, detail="Password salah bro")

    access_token = create_access_token(data={"sub": admin["email"], "role": admin["role"]})
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "email": admin["email"],
        "nama": admin["nama"]
    }

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token invalid")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid")
    
    result = db.execute(text("SELECT * FROM admins WHERE email = :email"), {"email": email})
    admin = result.mappings().first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin gak ketemu")
    return admin

@router.get("/me")
def read_users_me(current_user = Depends(get_current_user)):
    return {"email": current_user["email"], "nama": current_user["nama"], "role": current_user["role"]}
