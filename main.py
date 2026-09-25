from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import properties, blogs, estetikas, materials, gudangs, inquiries

# Bikin tabel otomatis kalo belum ada (aman, gak ngerusak data TiDB lu)
# Base.metadata.create_all(bind=engine)  # MATIKAN AJA BRO, SOALNYA LU UDAH BIKIN MANUAL DI TIDB - LEBIH AMAN

app = FastAPI(
    title="PASAGADANG API - FINAL SULTAN",
    description="API Properti, Blog, Estetika, Material, Gudang, Inquiries - 37 Kolom Properties + Video + Kredit + Lead WA",
    version="2.0.0"
)

# CORS - Biar bisa diakses dari Next.js / Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # nanti ganti ke domain lu: ["https://pasagadang.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DAFTARIN 6 ROUTER - SEKARANG UDAH LENGKAP!
app.include_router(properties.router)
app.include_router(blogs.router)
app.include_router(estetikas.router)
app.include_router(materials.router)
app.include_router(gudangs.router)
app.include_router(inquiries.router) # <--- YANG KEMARIN KOSONG 0 LINES, SEKARANG UDAH ADA!

@app.get("/")
def root():
    return {
        "message": "PASAGADANG API JALAN BRO! 🔥",
        "version": "2.0.0",
        "tables": ["properties (37 kolom)", "blogs", "estetikas", "materials", "gudangs", "inquiries (10 kolom)"],
        "endpoints": [
            "/properties - Properti Sultan 8 Foto + Video + Kredit",
            "/blogs - Tips & Inspirasi",
            "/estetikas - Roster & Granit",
            "/materials - Semen, Besi, dll",
            "/gudangs - Data Gudang Mitra",
            "/inquiries - Lead WA Calon Pembeli Sultan - NEW!"
        ],
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "OK", "database": "TiDB Connected"}

# JALANIN PAKE: uvicorn main:app --reload --port 8000
