
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/materials", tags=["Materials"])

@router.post("/", response_model=schemas.MaterialResponse)
def create_material(payload: schemas.MaterialCreate, db: Session = Depends(get_db)):
    if not payload.slug:
        payload.slug = models.Material.generate_slug(payload.nama)
    new_item = models.Material(**payload.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=list[schemas.MaterialResponse])
def list_material(kategori: str = None, brand: str = None, db: Session = Depends(get_db)):
    q = db.query(models.Material).filter(models.Material.is_active == True)
    if kategori:
        q = q.filter(models.Material.kategori == kategori)
    if brand:
        q = q.filter(models.Material.brand == brand)
    return q.all()
