from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ================== GUDANG ==================
class GudangBase(BaseModel):
    name: str
    alamat: Optional[str] = None
    kecamatan: Optional[str] = None
    tipe: Optional[str] = 'mitra'
    pic_name: Optional[str] = None
    wa_pic: Optional[str] = None
    share_stock_level: Optional[bool] = False
    is_active: Optional[bool] = True

class GudangCreate(GudangBase):
    pass

class GudangResponse(GudangBase):
    id: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ================== ESTETIKA ==================
class EstetikaBase(BaseModel):
    nama: str
    kategori: str
    slug: Optional[str] = None
    foto_bahan_1: Optional[str] = None
    foto_bahan_2: Optional[str] = None
    foto_bahan_3: Optional[str] = None
    foto_jadi_1: Optional[str] = None
    foto_jadi_2: Optional[str] = None
    foto_jadi_3: Optional[str] = None
    spesifikasi: Optional[str] = None
    ukuran: Optional[str] = None
    harga: int = 0
    satuan: Optional[str] = 'pcs'
    wa_number: Optional[str] = None
    deskripsi: Optional[str] = None
    badge: Optional[str] = None
    harga_promo: Optional[int] = None
    promo_sampai: Optional[datetime] = None
    is_active: Optional[bool] = True

class EstetikaCreate(EstetikaBase):
    pass

class EstetikaResponse(EstetikaBase):
    id: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ================== MATERIAL ==================
class MaterialBase(BaseModel):
    nama: str
    kategori: str
    slug: Optional[str] = None
    brand: Optional[str] = None
    foto_1: Optional[str] = None
    foto_2: Optional[str] = None
    foto_3: Optional[str] = None
    spesifikasi: Optional[str] = None
    ukuran: Optional[str] = None
    harga: int = 0
    satuan: str = 'pcs'
    stok_minimum: Optional[int] = 10
    wa_number: Optional[str] = None
    deskripsi: Optional[str] = None
    badge: Optional[str] = None
    harga_promo: Optional[int] = None
    promo_sampai: Optional[datetime] = None
    is_active: Optional[bool] = True

class MaterialCreate(MaterialBase):
    pass

class MaterialResponse(MaterialBase):
    id: int
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ================== BLOG ==================
class BlogBase(BaseModel):
    judul: str
    slug: Optional[str] = None
    kategori: str
    thumbnail: Optional[str] = None
    excerpt: Optional[str] = None
    konten: str
    tags: Optional[str] = None
    author_name: Optional[str] = 'Admin Pasagadang'
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    views: Optional[int] = 0
    is_published: Optional[bool] = False
    published_at: Optional[datetime] = None

class BlogCreate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

# ================== PROPERTY - FINAL SULTAN 37 KOLOM ==================
class PropertyBase(BaseModel):
    judul: str
    slug: Optional[str] = None
    tipe_properti: str
    tipe_transaksi: str = 'jual'

    # HARGA CASH & KREDIT
    harga_cash: int = 0
    harga_kredit: Optional[int] = None
    dp: Optional[int] = None
    cicilan_per_bulan: Optional[int] = None
    tenor_bulan: Optional[int] = None
    harga_sewa_per: Optional[str] = None

    alamat: Optional[str] = None
    kecamatan: Optional[str] = None
    luas_tanah: Optional[int] = 0
    luas_bangunan: Optional[int] = 0
    kamar_tidur: Optional[int] = 0
    kamar_mandi: Optional[int] = 0
    sertifikat: Optional[str] = 'SHM'

    # 8 FOTO + VIDEO
    thumbnail: Optional[str] = None
    foto_1: Optional[str] = None
    foto_2: Optional[str] = None
    foto_3: Optional[str] = None
    foto_4: Optional[str] = None
    foto_5: Optional[str] = None
    foto_6: Optional[str] = None
    foto_7: Optional[str] = None
    foto_8: Optional[str] = None
    video_url: Optional[str] = None
    video_thumbnail: Optional[str] = None

    deskripsi: Optional[str] = None
    fasilitas: Optional[str] = None
    wa_number: Optional[str] = None
    badge: Optional[str] = None
    views: Optional[int] = 0
    is_published: Optional[bool] = False

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    judul: Optional[str] = None
    slug: Optional[str] = None
    tipe_properti: Optional[str] = None
    tipe_transaksi: Optional[str] = None
    harga_cash: Optional[int] = None
    harga_kredit: Optional[int] = None
    dp: Optional[int] = None
    cicilan_per_bulan: Optional[int] = None
    tenor_bulan: Optional[int] = None
    harga_sewa_per: Optional[str] = None
    alamat: Optional[str] = None
    kecamatan: Optional[str] = None
    luas_tanah: Optional[int] = None
    luas_bangunan: Optional[int] = None
    kamar_tidur: Optional[int] = None
    kamar_mandi: Optional[int] = None
    sertifikat: Optional[str] = None
    thumbnail: Optional[str] = None
    foto_1: Optional[str] = None
    foto_2: Optional[str] = None
    foto_3: Optional[str] = None
    foto_4: Optional[str] = None
    foto_5: Optional[str] = None
    foto_6: Optional[str] = None
    foto_7: Optional[str] = None
    foto_8: Optional[str] = None
    video_url: Optional[str] = None
    video_thumbnail: Optional[str] = None
    deskripsi: Optional[str] = None
    fasilitas: Optional[str] = None
    wa_number: Optional[str] = None
    badge: Optional[str] = None
    is_published: Optional[bool] = None

class PropertyResponse(PropertyBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
