from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/gudangs", tags=["Gudangs"])

@router.post("/", response_model=schemas.GudangResponse)
def create_gudang(payload: schemas.GudangCreate, db: Session = Depends(get_db)):
    new_item = models.Gudang(**payload.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=list[schemas.GudangResponse])
def list_gudang(db: Session = Depends(get_db)):
    return db.query(models.Gudang).filter(models.Gudang.is_active == True).all()
