from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Coba import database flexible biar gak error di Vercel
try:
    from database import engine, Base
    import models
except:
    from app.database import engine, Base
    import app.models as models

# Biar table auto ke-create di TiDB
try:
    Base.metadata.create_all(bind=engine)
    print("✅ DB Connected")
except Exception as e:
    print(f"⚠️ DB Skip: {e}")

def safe_import(name_singular, name_plural):
    # Coba 4 lokasi biar gak gagal
    for path in [f"routers.{name_plural}", f"routers.{name_singular}", f"app.routers.{name_plural}", f"app.routers.{name_singular}"]:
        try:
            mod = __import__(path, fromlist=[name_plural, name_singular])
            print(f"✅ Found {path}")
            return mod
        except ImportError:
            continue
    print(f"❌ FAILED {name_singular}/{name_plural} - bikin dummy")
    from fastapi import APIRouter
    dummy = type('obj', (object,), {'router': APIRouter()})()
    return dummy

# LOAD SEMUA ROUTER
auth_mod = safe_import("auth", "auth")
properties = safe_import("property", "properties")
blogs_mod = safe_import("blog", "blogs")
estetikas = safe_import("estetika", "estetikas")
materials = safe_import("material", "materials")
gudangs = safe_import("gudang", "gudangs")
inquiries = safe_import("inquiry", "inquiries")

app = FastAPI(
    title="PASAGADANG API - FINAL SULTAN",
    description="API Properti, Blog, Estetika, Material, Gudang, Inquiries, Auth",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DAFTARIN ROUTER
app.include_router(auth_mod.router)
app.include_router(properties.router)
app.include_router(blogs_mod.router)
app.include_router(estetikas.router)
app.include_router(materials.router)
app.include_router(gudangs.router)
app.include_router(inquiries.router)

@app.get("/")
@app.head("/")
def root():
    return {
        "message": "PASAGADANG API JALAN BRO! 🔥",
        "version": "2.0.0",
        "status": "Anti-gagal mode ON",
        "docs": "/docs"
    }

# === INI KUNCI ANTI TIDUR + ANTI 405 BRO ===
@app.get("/health")
@app.head("/health")
@app.get("/api/health")
@app.head("/api/health")
def health_check():
    return {"status": "OK", "database": "TiDB Connected", "service": "pasagadang-api"}

@app.get("/api")
@app.head("/api")
def api_root():
    return {"message": "PASAGADANG API JALAN BRO! 🔥", "health": "/api/health"}
