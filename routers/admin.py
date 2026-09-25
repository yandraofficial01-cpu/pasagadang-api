from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models
from routers.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Hitung total data
    total_properties = db.query(func.count(models.Property.id)).scalar()
    total_blogs = db.query(func.count(models.Blog.id)).scalar()
    total_materials = db.query(func.count(models.Material.id)).scalar()
    total_estetikas = db.query(func.count(models.Estetika.id)).scalar()
    total_gudangs = db.query(func.count(models.Gudang.id)).scalar()

    # Hitung yang published
    properties_published = db.query(func.count(models.Property.id)).filter(models.Property.is_published == True).scalar()
    properties_draft = total_properties - properties_published

    # Total views properties
    total_views = db.query(func.sum(models.Property.views)).scalar() or 0

    # Properti terbaru
    latest_properties = db.query(models.Property).order_by(models.Property.created_at.desc()).limit(5).all()

    return {
        "total": {
            "properties": total_properties,
            "blogs": total_blogs,
            "materials": total_materials,
            "estetikas": total_estetikas,
            "gudangs": total_gudangs
        },
        "properties": {
            "published": properties_published,
            "draft": properties_draft,
            "total_views": total_views
        },
        "latest_properties": [
            {"id": p.id, "judul": p.judul, "slug": p.slug, "views": p.views, "is_published": p.is_published}
            for p in latest_properties
        ],
        "message": "Dashboard Sultan Pasagadang"
    }

@router.get("/properties/draft")
def get_draft_properties(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    drafts = db.query(models.Property).filter(models.Property.is_published == False).order_by(models.Property.created_at.desc()).all()
    return drafts

@router.get("/properties/popular")
def get_popular_properties(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    popular = db.query(models.Property).order_by(models.Property.views.desc()).limit(10).all()
    return popular
