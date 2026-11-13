from fastapi import APIRouter, Depends, HTTPException
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
def list_estetika(kategori: str = None, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    q = db.query(models.Estetika).filter(models.Estetika.is_active == True)
    if kategori:
        q = q.filter(models.Estetika.kategori == kategori)
    return q.order_by(models.Estetika.created_at.desc()).limit(limit).offset(offset).all()

@router.put("/{estetika_id}", response_model=schemas.EstetikaResponse)
@router.patch("/{estetika_id}", response_model=schemas.EstetikaResponse)
def update_estetika(estetika_id: int, payload: schemas.EstetikaCreate, db: Session = Depends(get_db)):
    item = db.query(models.Estetika).filter(models.Estetika.id == estetika_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Estetika not found")
    data = payload.model_dump(exclude_unset=True)
    if "nama" in data and not data.get("slug"):
        data["slug"] = models.Estetika.generate_slug(data["nama"])
    for key, value in data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{estetika_id}")
def delete_estetika(estetika_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Estetika).filter(models.Estetika.id == estetika_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Estetika not found")
    db.delete(item)
    db.commit()
    return {"ok": True, "deleted_id": estetika_id}
