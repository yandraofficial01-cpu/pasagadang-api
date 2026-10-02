from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from ai import generate_all_in_one  # <-- V3 BRAIN MASUK SINI BRO

def safe_import(name_singular, name_plural):
    try:
        mod = __import__(f"routers.{name_plural}", fromlist=[name_plural])
        print(f"✅ Found routers.{name_plural}.py")
        return mod
    except ImportError:
        try:
            mod = __import__(f"routers.{name_singular}", fromlist=[name_singular])
            print(f"✅ Found routers.{name_singular}.py as {name_plural}")
            return mod
        except ImportError as e:
            print(f"❌ FAILED {name_singular}/{name_plural}: {e}")
            from fastapi import APIRouter
            dummy = type('obj', (object,), {'router': APIRouter()})()
            return dummy

# TAMBAH AUTH DISINI BRO!
auth_mod = safe_import("auth", "auth")
properties = safe_import("property", "properties")
blogs_mod = safe_import("blog", "blogs")
estetikas = safe_import("estetika", "estetikas")
materials = safe_import("material", "materials")
gudangs = safe_import("gudang", "gudangs")
inquiries = safe_import("inquiry", "inquiries")

app = FastAPI(
    title="PASAGADANG API - FINAL SULTAN V3",
    description="API Properti, Blog, Estetika, Material, Gudang, Inquiries, Auth + AI V3",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DAFTARIN - JANGAN LUPA AUTH!
app.include_router(auth_mod.router)
app.include_router(properties.router)
app.include_router(blogs_mod.router)
app.include_router(estetikas.router)
app.include_router(materials.router)
app.include_router(gudangs.router)
app.include_router(inquiries.router)

@app.get("/")
def root():
    return {
        "message": "PASAGADANG API JALAN BRO! 🔥 V3",
        "version": "3.0.0",
        "status": "Anti-gagal + AI V3 ON",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "OK", "database": "TiDB Connected"}

# ================== AI V3 ENDPOINT - GAS BRO! ==================
@app.post("/ai/generate-v3/")
def gen_v3(nama: str, kategori: str, harga: int, tipe: str = "properti"):
    """
    V3 SUPER BRAIN - 1 KLIK JADI 4
    tipe: properti / estetika / material
    contoh: /ai/generate-v3/?nama=Roster Mawar&kategori=20x20&harga=25000&tipe=estetika
    """
    try:
        hasil = generate_all_in_one(nama, kategori, harga, tipe, harga_pasaran=harga+10000)
        return {"status": "sukses", "data": hasil}
    except Exception as e:
        return {"status": "gagal", "error": str(e)}

@app.post("/ai/blog/")
def gen_blog(topik: str):
    """Generate artikel blog 600 kata otomatis"""
    from ai import generate_blog_post
    try:
        artikel = generate_blog_post(topik)
        return {"status": "sukses", "topik": topik, "artikel": artikel}
    except Exception as e:
        return {"status": "gagal", "error": str(e)}
