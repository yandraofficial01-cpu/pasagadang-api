from sqlalchemy import Column, Integer, String, BigInteger, Text, TIMESTAMP, func, Boolean
from database import Base
import re

class Gudang(Base):
    __tablename__ = "gudangs"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    alamat = Column(Text, nullable=True)
    kecamatan = Column(String(50), nullable=True, index=True)
    tipe = Column(String(20), default='mitra', index=True)
    pic_name = Column(String(100), nullable=True)
    wa_pic = Column(String(20), nullable=True)
    share_stock_level = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Estetika(Base):
    __tablename__ = "estetikas"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nama = Column(String(150), nullable=False)
    kategori = Column(String(50), nullable=False, index=True) # roster, granit, batu_alam
    slug = Column(String(200), unique=True, nullable=False, index=True)
    
    # 6 Foto - 3 Bahan + 3 Jadi
    foto_bahan_1 = Column(Text, nullable=True)
    foto_bahan_2 = Column(Text, nullable=True)
    foto_bahan_3 = Column(Text, nullable=True)
    foto_jadi_1 = Column(Text, nullable=True)
    foto_jadi_2 = Column(Text, nullable=True)
    foto_jadi_3 = Column(Text, nullable=True)
    
    spesifikasi = Column(Text, nullable=True)
    ukuran = Column(String(50), nullable=True)
    harga = Column(Integer, nullable=False, default=0)
    satuan = Column(String(20), default='pcs')
    wa_number = Column(String(20), nullable=True)
    deskripsi = Column(Text, nullable=True)
    
    # Badge Promo
    badge = Column(String(20), nullable=True, index=True) # PROMO, BEST SELLER, BARU
    harga_promo = Column(Integer, nullable=True)
    promo_sampai = Column(TIMESTAMP, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    @staticmethod
    def generate_slug(nama: str):
        slug = nama.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        return slug.strip('-')

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    nama = Column(String(150), nullable=False)
    kategori = Column(String(50), nullable=False, index=True) # semen, besi, bata, pasir, kayu
    slug = Column(String(200), unique=True, nullable=False, index=True)
    brand = Column(String(100), nullable=True, index=True) # Semen Padang, Krakatau Steel
    
    # 3 Foto aja, gak perlu foto jadi
    foto_1 = Column(Text, nullable=True)
    foto_2 = Column(Text, nullable=True)
    foto_3 = Column(Text, nullable=True)
    
    spesifikasi = Column(Text, nullable=True)
    ukuran = Column(String(50), nullable=True)
    harga = Column(Integer, nullable=False, default=0)
    satuan = Column(String(30), nullable=False, default='pcs') # BEBAS: sak, batang, buah, m3, truk, lembar, kg, liter
    stok_minimum = Column(Integer, default=10)
    wa_number = Column(String(20), nullable=True)
    deskripsi = Column(Text, nullable=True)
    
    # Badge Promo
    badge = Column(String(20), nullable=True, index=True) # PROMO, BEST SELLER, BARU
    harga_promo = Column(Integer, nullable=True)
    promo_sampai = Column(TIMESTAMP, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    @staticmethod
    def generate_slug(nama: str):
        slug = nama.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        return slug.strip('-')

class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    judul = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    kategori = Column(String(50), nullable=False, index=True) # tips, inspirasi, promo, berita
    thumbnail = Column(Text, nullable=True) # cover utama
    excerpt = Column(String(300), nullable=True)
    konten = Column(Text, nullable=False) # LONGTEXT - isi full, foto selipin di sini pake <img>
    tags = Column(String(200), nullable=True)
    author_name = Column(String(100), default='Admin Pasagadang')
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(String(300), nullable=True)
    views = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    published_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    @staticmethod
    def generate_slug(judul: str):
        slug = judul.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        return slug.strip('-')

# ================== TABEL BARU BRO - FINAL SULTAN ==================
class Property(Base):
    __tablename__ = "properties"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    judul = Column(String(200), nullable=False)
    slug = Column(String(250), unique=True, nullable=False, index=True)
    tipe_properti = Column(String(50), nullable=False, index=True) # rumah, tanah, ruko, gudang, kos, apartemen
    tipe_transaksi = Column(String(20), nullable=False, default='jual', index=True) # jual, sewa

    # HARGA CASH & KREDIT - FITUR BARU!
    harga_cash = Column(BigInteger, nullable=False, default=0)
    harga_kredit = Column(BigInteger, nullable=True)
    dp = Column(BigInteger, nullable=True) # DP minimal
    cicilan_per_bulan = Column(BigInteger, nullable=True)
    tenor_bulan = Column(Integer, nullable=True) # 120 bulan = 10 tahun
    harga_sewa_per = Column(String(20), nullable=True) # bulan, tahun

    alamat = Column(Text, nullable=True)
    kecamatan = Column(String(50), nullable=True, index=True)
    luas_tanah = Column(Integer, default=0)
    luas_bangunan = Column(Integer, default=0)
    kamar_tidur = Column(Integer, default=0)
    kamar_mandi = Column(Integer, default=0)
    sertifikat = Column(String(20), default='SHM')
    
    # MEDIA 8 FOTO + VIDEO
    thumbnail = Column(Text, nullable=True)
    foto_1 = Column(Text, nullable=True)
    foto_2 = Column(Text, nullable=True)
    foto_3 = Column(Text, nullable=True)
    foto_4 = Column(Text, nullable=True)
    foto_5 = Column(Text, nullable=True)
    foto_6 = Column(Text, nullable=True)
    foto_7 = Column(Text, nullable=True)
    foto_8 = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True) # youtube / tiktok
    video_thumbnail = Column(Text, nullable=True)

    deskripsi = Column(Text, nullable=True) # LONGTEXT di TiDB
    fasilitas = Column(Text, nullable=True) # AC, Carport, PDAM, 2200W
    wa_number = Column(String(20), nullable=True)
    badge = Column(String(20), nullable=True) # BARU, PROMO, TERJUAL
    views = Column(Integer, default=0)
    is_published = Column(Boolean, default=False, index=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    @staticmethod
    def generate_slug(judul: str):
        slug = judul.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        return slug.strip('-')
