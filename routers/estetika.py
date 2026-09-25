from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/estetikas", tags=["Estetika"])

@router.post("/", response_model=schemas.EstetikaResponse)
def create_estetika(payload: schemas.EstetikaCreate, db: Session = Depends(get_db)):
    if not payload.slug:
        payload.slug = models.Estetika.generate_slug(payload.nama)
    new_item = models.Estetika(**payload.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=list[schemas.EstetikaResponse])
def list_estetika(kategori: str = None, db: Session = Depends(get_db)):
    q = db.query(models.Estetika).filter(models.Estetika.is_active == True)
    if kategori:
        q = q.filter(models.Estetika.kategori == kategori)
    return q.all()
