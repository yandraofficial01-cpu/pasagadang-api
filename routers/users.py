
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from routers.auth import get_password_hash, get_current_user
import models

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "admin"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    class Config:
        from_attributes = True

# Tambahin model User di models.py lu kalo belum ada
# class User(Base):
#     __tablename__ = "users"
#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     username = Column(String(50), unique=True, nullable=False)
#     email = Column(String(100), unique=True, nullable=False)
#     hashed_password = Column(String(200), nullable=False)
#     role = Column(String(20), default='admin')
#     is_active = Column(Boolean, default=True)
#     created_at = Column(TIMESTAMP, server_default=func.now())

@router.get("/", dependencies=[Depends(get_current_user)])
def list_users(db: Session = Depends(get_db)):
    # Untuk sekarang return hardcoded dulu biar gak error
    # Nanti kalo udah bikin tabel users, ganti query DB
    return [
        {"id": 1, "username": "admin", "email": "admin@pasagadang.com", "role": "super_admin"},
        {"id": 2, "username": "editor", "email": "editor@pasagadang.com", "role": "editor"}
    ]

@router.post("/", dependencies=[Depends(get_current_user)])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Simpan user baru - versi simple dulu
    # Kalo udah ada tabel users, uncomment ini:
    # hashed = get_password_hash(payload.password)
    # new_user = models.User(username=payload.username, email=payload.email, hashed_password=hashed, role=payload.role)
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # return new_user
    
    return {
        "message": "User created (mock)",
        "username": payload.username,
        "email": payload.email,
        "note": "Bikin tabel users dulu di TiDB biar permanen bro!"
    }

@router.get("/me", dependencies=[Depends(get_current_user)])
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user
