from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models, schemas
import os, uuid, re
from datetime import datetime
import cloudinary
import cloudinary.uploader

router = APIRouter(prefix="/blogs", tags=["Blogs"])

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

IKLAN_CONFIG = {
    "top": {"kode_adsense": None, "gambar": "/ads/rendang-promo.jpg", "link": "/promo", "active": True},
    "middle": {"kode_adsense": None, "gambar": "/ads/dendeng.jpg", "link": "/promo", "active": True},
    "sidebar": {"kode_adsense": None, "gambar": "/ads/sidebar.jpg", "link": "/promo", "active": True}
}

# FIX VERCEL READ-ONLY - INI UDAH BENER
UPLOAD_DIR = "/tmp/blogs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("", response_model=schemas.BlogResponse)
def create_blog(payload: schemas.BlogCreate, db: Session = Depends(get_db)):
    if not payload.slug:
        payload.slug = models.Blog.generate_slug(payload.judul)
    if not payload.meta_title:
        payload.meta_title = payload.judul[:60]
    if not payload.meta_description and payload.excerpt:
        payload.meta_description = payload.excerpt[:160]
    elif not payload.meta_description:
        clean = re.sub(r'<[^>]+>', '', payload.konten)[:160]
        payload.meta_description = clean
    existing = db.query(models.Blog).filter(models.Blog.slug == payload.slug).first()
    if existing:
        payload.slug = f"{payload.slug}-{uuid.uuid4().hex[:4]}"
    data = payload.model_dump()
    if data.get("is_published") and not data.get("published_at"):
        data["published_at"] = datetime.now()
    new_blog = models.Blog(**data)
    db.add(new_blog); db.commit(); db.refresh(new_blog)
    return new_blog

@router.post("/upload-image")
def upload_gambar(file: UploadFile = File(...)):
    try:
        result = cloudinary.uploader.upload(file.file, folder="pasagadang/blogs")
        return {"url": result["secure_url"]}
    except Exception as e:
        # JANGAN RAISE kalau cloudinary belum set, kasih log aja
        print(f"Cloudinary error: {e}")
        # fallback darurat ke /tmp (di vercel ini hilang setelah request, jadi cuma buat debug)
        try:
            ext = file.filename.split(".")[-1]
            fname = f"{uuid.uuid4().hex}.{ext}"
            path = os.path.join(UPLOAD_DIR, fname)
            with open(path, "wb") as f:
                f.write(file.file.read())
            return {"url": f"/tmp/blogs/{fname}", "warning": "cloudinary belum setting, file di /tmp"}
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Upload gagal: {str(ex)}")

@router.get("/", response_model=list[schemas.BlogResponse])
def list_blogs(kategori: str = None, all: bool = False, db: Session = Depends(get_db)):
    q = db.query(models.Blog)
    if not all:
        q = q.filter(models.Blog.is_published == True)
    if kategori:
        q = q.filter(models.Blog.kategori == kategori)
    return q.order_by(models.Blog.created_at.desc()).all()

@router.get("/sitemap.xml")
def sitemap(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.is_published == True).all()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for b in blogs:
        xml += f"  <url><loc>https://pasagadang.com/blog/{b.slug}</loc><lastmod>{b.updated_at.date() if b.updated_at else b.created_at.date()}</lastmod></url>\n"
    xml += "</urlset>"
    return Response(content=xml, media_type="application/xml")

@router.put("/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(blog_id: int, payload: schemas.BlogCreate, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog: raise HTTPException(404, "Blog tidak ditemukan")
    for k,v in payload.model_dump(exclude_unset=True).items():
        setattr(blog, k, v)
    blog.updated_at = datetime.now()
    db.commit(); db.refresh(blog)
    return blog

@router.delete("/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog: raise HTTPException(404, "Blog tidak ditemukan")
    db.delete(blog); db.commit()
    return {"message": "Hapus sukses"}

@router.get("/{slug}")
def detail_blog(slug: str, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.slug == slug).first()
    if not blog: raise HTTPException(404, "Blog tidak ditemukan")
    blog.views += 1; db.commit()
    related = db.query(models.Blog).filter(
        models.Blog.kategori == blog.kategori,
        models.Blog.id != blog.id,
        models.Blog.is_published == True
    ).order_by(func.random()).limit(3).all()
    return {"blog": blog, "baca_juga": related, "iklan": IKLAN_CONFIG}
