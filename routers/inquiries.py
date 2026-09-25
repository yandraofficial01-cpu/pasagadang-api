from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Inquiry, Property
import datetime

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])

# ===== SCHEMAS =====
class InquiryCreate(BaseModel):
    nama: str
    whatsapp: str
    pesan: str
    property_id: Optional[int] = None
    property_slug: Optional[str] = None
    sumber: Optional[str] = "website"

class InquiryUpdateStatus(BaseModel):
    status: str # new, contacted, closing, sold, batal

class InquiryResponse(BaseModel):
    id: int
    property_id: Optional[int] = None
    property_slug: Optional[str] = None
    nama: str
    whatsapp: str
    pesan: str
    sumber: str
    status: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

# ===== CREATE - DARI WEBSITE =====
@router.post("/", response_model=InquiryResponse)
def create_inquiry(data: InquiryCreate, db: Session = Depends(get_db)):
    # Kalo ada slug, coba cari property_id biar double aman
    prop_id = data.property_id
    if data.property_slug and not prop_id:
        prop = db.query(Property).filter(Property.slug == data.property_slug).first()
        if prop:
            prop_id = prop.id

    new_inquiry = Inquiry(
        property_id=prop_id,
        property_slug=data.property_slug,
        nama=data.nama,
        whatsapp=data.whatsapp,
        pesan=data.pesan,
        sumber=data.sumber,
        status="new"
    )
    db.add(new_inquiry)
    db.commit()
    db.refresh(new_inquiry)
    return new_inquiry

# ===== GET ALL - BUAT ADMIN =====
@router.get("/", response_model=List[InquiryResponse])
def get_all_inquiries(
    status: Optional[str] = None,
    property_slug: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Inquiry).order_by(Inquiry.created_at.desc())
    if status:
        query = query.filter(Inquiry.status == status)
    if property_slug:
        query = query.filter(Inquiry.property_slug == property_slug)

    return query.offset(skip).limit(limit).all()

# ===== GET ONE =====
@router.get("/{inquiry_id}", response_model=InquiryResponse)
def get_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry tidak ditemukan")
    return inquiry

# ===== UPDATE STATUS - WA UDAH? CLOSING? SOLD? =====
@router.patch("/{inquiry_id}", response_model=InquiryResponse)
def update_status(inquiry_id: int, data: InquiryUpdateStatus, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry tidak ditemukan")

    # Validasi status biar gak ngawur
    allowed = ["new", "contacted", "closing", "sold", "batal"]
    if data.status not in allowed:
        raise HTTPException(status_code=400, detail=f"Status harus salah satu: {', '.join(allowed)}")

    inquiry.status = data.status
    # updated_at auto ke-update sama TiDB ON UPDATE CURRENT_TIMESTAMP!
    db.commit()
    db.refresh(inquiry)
    return inquiry

# ===== DELETE =====
@router.delete("/{inquiry_id}")
def delete_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry tidak ditemukan")
    db.delete(inquiry)
    db.commit()
    return {"message": f"Inquiry {inquiry_id} berhasil dihapus"}
