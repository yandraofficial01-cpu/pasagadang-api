from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, uuid

router = APIRouter(prefix="/properties", tags=["Properties"])

def make_unique_slug(db, judul: str, current_id=None):
    base = models.Property.generate_slug(judul)[:50]
    slug = base
    q = db.query(models.Property).filter(models.Property.slug == slug)
    if current_id:
        q = q.filter(models.Property.id != current_id)
    # kalau udah ada, kasih random
    if q.first():
        slug = f"{base}-{uuid.uuid4().hex[:4]}"
    return slug

@router.post("/", response_model=schemas.PropertyResponse)
def create_property(payload: schemas.PropertyCreate, db: Session = Depends(get_db)):
    if not payload.slug:
        payload.slug = make_unique_slug(db, payload.judul)
    else:
        # pastiin unik juga
        payload.slug = make_unique_slug(db, payload.slug)
        
    new_prop = models.Property(**payload.model_dump())
    db.add(new_prop)
    try:
        db.commit()
    except Exception:
        db.rollback()
        # fallback terakhir anti-duplicate
        new_prop.slug = f"{new_prop.slug}-{uuid.uuid4().hex[:6]}"
        db.add(new_prop)
        db.commit()
    db.refresh(new_prop)
    return new_prop

@router.get("/", response_model=list[schemas.PropertyResponse])
def list_properties(kecamatan: str = None, tipe: str = None, transaksi: str = None, is_admin: bool = False, db: Session = Depends(get_db)):
    # kalau admin, kasih semua. kalau public, cuma published
    q = db.query(models.Property)
    if not is_admin:
        q = q.filter(models.Property.is_published == True)
    if kecamatan:
        q = q.filter(models.Property.kecamatan == kecamatan)
    if tipe:
        q = q.filter(models.Property.tipe_properti == tipe)
    if transaksi:
        q = q.filter(models.Property.tipe_transaksi == transaksi)
    return q.order_by(models.Property.created_at.desc()).all()

# HARUS di bawah, biar gak nabrak ID
@router.put("/{id}", response_model=schemas.PropertyResponse)
def update_property(id: int, payload: schemas.PropertyUpdate, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == id).first()
    if not prop:
        raise HTTPException(404, "Not found")
    data = payload.model_dump(exclude_unset=True)
    if "judul" in data and data["judul"]:
        data["slug"] = make_unique_slug(db, data["judul"], current_id=id)
    for k, v in data.items():
        setattr(prop, k, v)
    db.commit()
    db.refresh(prop)
    return prop

@router.delete("/{id}")
def delete_property(id: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == id).first()
    if not prop:
        raise HTTPException(404, "Not found")
    db.delete(prop)
    db.commit()
    return {"message": "Deleted"}

@router.get("/{slug}", response_model=schemas.PropertyResponse)
def detail_property(slug: str, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.slug == slug).first()
    if not prop:
        raise HTTPException(404, "Properti tidak ditemukan")
    prop.views += 1
    db.commit()
    return prop
