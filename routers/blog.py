
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.post("/", response_model=schemas.BlogResponse)
def create_blog(payload: schemas.BlogCreate, db: Session = Depends(get_db)):
    if not payload.slug:
        payload.slug = models.Blog.generate_slug(payload.judul)
    new_blog = models.Blog(**payload.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/", response_model=list[schemas.BlogResponse])
def list_blogs(kategori: str = None, db: Session = Depends(get_db)):
    q = db.query(models.Blog).filter(models.Blog.is_published == True)
    if kategori:
        q = q.filter(models.Blog.kategori == kategori)
    return q.order_by(models.Blog.created_at.desc()).all()

@router.get("/{slug}", response_model=schemas.BlogResponse)
def detail_blog(slug: str, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.slug == slug).first()
    if not blog:
        raise HTTPException(404, "Blog tidak ditemukan")
    blog.views += 1
    db.commit()
    return blog
