from sqlalchemy import Column, Integer, String, BigInteger, Text, TIMESTAMP, func, Boolean
from database import Base

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
