
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import get_db
import models
import os

router = APIRouter(prefix="/auth", tags=["Auth"])

# SECRET KEY - GANTI DI RENDER ENV!
SECRET_KEY = os.getenv("SECRET_KEY", "pasagadang-sultan-key-2026-ganti-di-render")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 hari

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Cari di tabel users (lu harus bikin tabel users dulu bro)
    # Untuk sementara hardcode admin dulu
    if username == "admin":
        return {"username": "admin", "role": "admin"}
    raise credentials_exception

# ADMIN LOGIN - HARDCODE DULU BIAR CEPET
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = get_password_hash(os.getenv("ADMIN_PASSWORD", "pasagadang123"))

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Cek username
    if form_data.username != ADMIN_USERNAME:
        raise HTTPException(status_code=400, detail="Username salah")
    if not verify_password(form_data.password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=400, detail="Password salah")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer", "username": form_data.username}

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
