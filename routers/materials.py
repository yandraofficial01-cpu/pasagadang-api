from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/{id_or_slug}", response_model=schemas.MaterialResponse)
def get_material(id_or_slug: str, db: Session = Depends(get_db)):
    q = db.query(models.Material).filter(models.Material.is_active == True)

    # 1. coba by ID angka: /materials/123
    if id_or_slug.isdigit():
        item = q.filter(models.Material.id == int(id_or_slug)).first()
        if item:
            return item

    # 2. coba by SLUG asli: /materials/semen-gresik-50kg -> SEO TERBAIK
    item = q.filter(models.Material.slug == id_or_slug).first()
    if item:
        return item

    # 3. coba by ID-SLUG: /materials/123-semen-gresik-50kg
    if "-" in id_or_slug:
        try:
            _id = int(id_or_slug.split("-")[0])
            item = q.filter(models.Material.id == _id).first()
            if item:
                return item
        except:
            pass

    raise HTTPException(status_code=404, detail="Material not found")
