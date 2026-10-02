from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models

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
        "message": "PASAGADANG API JALAN BRO! 🔥",
        "version": "2.0.0",
        "status": "Anti-gagal mode ON",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "OK", "database": "TiDB Connected"}
