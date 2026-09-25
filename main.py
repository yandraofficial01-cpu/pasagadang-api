from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import properties, blogs, estetikas, materials, gudangs

# Bikin tabel otomatis kalo belum ada (aman, gak ngerusak data TiDB lu)
# Base.metadata.create_all(bind=engine)  # MATIKAN AJA BRO, SOALNYA LU UDAH BIKIN MANUAL DI TIDB - LEBIH AMAN

app = FastAPI(
    title="PASAGADANG API - FINAL SULTAN",
    description="API Properti, Blog, Estetika, Material, Gudang - 37 Kolom Properties + Video + Kredit",
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

# DAFTARIN 5 ROUTER
app.include_router(properties.router)
app.include_router(blogs.router)
app.include_router(estetikas.router)
app.include_router(materials.router)
app.include_router(gudangs.router)

@app.get("/")
def root():
    return {
        "message": "PASAGADANG API JALAN BRO! 🔥",
        "version": "2.0.0",
        "tables": ["properties (37 kolom)", "blogs", "estetikas", "materials", "gudangs"],
        "endpoints": [
            "/properties - Properti Sultan 8 Foto + Video + Kredit",
            "/blogs - Tips & Inspirasi",
            "/estetikas - Roster & Granit",
            "/materials - Semen, Besi, dll",
            "/gudangs - Data Gudang Mitra"
        ],
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "OK", "database": "TiDB Connected"}

# JALANIN PAKE: uvicorn main:app --reload --port 8000
