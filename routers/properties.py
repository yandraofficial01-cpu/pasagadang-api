
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=schemas.PropertyResponse)
def create_property(payload: schemas.PropertyCreate, db: Session = Depends(get_db)):
    if not payload.slug:
        payload.slug = models.Property.generate_slug(payload.judul)
    # cek slug duplikat
    if db.query(models.Property).filter(models.Property.slug == payload.slug).first():
        payload.slug = f"{payload.slug}-{models.Property.generate_slug(payload.judul)[:4]}"
    new_prop = models.Property(**payload.model_dump())
    db.add(new_prop)
    db.commit()
    db.refresh(new_prop)
    return new_prop

@router.get("/", response_model=list[schemas.PropertyResponse])
def list_properties(kecamatan: str = None, tipe: str = None, transaksi: str = None, db: Session = Depends(get_db)):
    q = db.query(models.Property).filter(models.Property.is_published == True)
    if kecamatan:
        q = q.filter(models.Property.kecamatan == kecamatan)
    if tipe:
        q = q.filter(models.Property.tipe_properti == tipe)
    if transaksi:
        q = q.filter(models.Property.tipe_transaksi == transaksi)
    return q.order_by(models.Property.created_at.desc()).all()

@router.get("/{slug}", response_model=schemas.PropertyResponse)
def detail_property(slug: str, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.slug == slug).first()
    if not prop:
        raise HTTPException(404, "Properti tidak ditemukan")
    prop.views += 1
    db.commit()
    return prop

@router.put("/{id}", response_model=schemas.PropertyResponse)
def update_property(id: int, payload: schemas.PropertyUpdate, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.id == id).first()
    if not prop:
        raise HTTPException(404, "Not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
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
