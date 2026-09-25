from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/calculator", tags=["Calculator"])

class HitungRequest(BaseModel):
    panjang: float # meter
    lebar: float # meter
    tinggi: Optional[float] = 3 # tinggi dinding
    jenis: str = "bata_merah" # bata_merah, batako, hebel

class SemenRequest(BaseModel):
    luas_dinding_m2: float
    ketebalan_plester_cm: float = 2

@router.post("/bata")
def hitung_bata(req: HitungRequest):
    luas_dinding = (req.panjang * req.tinggi * 2) + (req.lebar * req.tinggi * 2)

    # Standar kebutuhan per m2
    standar = {
        "bata_merah": 70, # buah per m2
        "batako": 12, # buah per m2
        "hebel": 8 # buah per m2
    }

    kebutuhan_per_m2 = standar.get(req.jenis, 70)
    total_bata = luas_dinding * kebutuhan_per_m2
    # tambah 5% waste
    total_bata_waste = total_bata * 1.05

    return {
        "luas_dinding_m2": round(luas_dinding, 2),
        "jenis_bata": req.jenis,
        "kebutuhan_per_m2": kebutuhan_per_m2,
        "total_dibutuhkan": int(total_bata),
        "total_dengan_waste_5%": int(total_bata_waste),
        "satuan": "buah"
    }

@router.post("/semen")
def hitung_semen(req: SemenRequest):
    # 1 sak semen (50kg) untuk ~ 6 m2 plester 2cm
    luas = req.luas_dinding_m2
    sak_dibutuhkan = luas / 6
    # pasir: 1 sak semen butuh 0.05 m3 pasir
    pasir_m3 = sak_dibutuhkan * 0.05

    return {
        "luas_dinding_m2": luas,
        "semen_50kg": round(sak_dibutuhkan, 1),
        "semen_50kg_bulatkan": int(sak_dibutuhkan) + 1,
        "pasir_m3": round(pasir_m3, 2),
        "catatan": "Untuk plester tebal {}cm".format(req.ketebalan_plester_cm)
    }

@router.get("/harga-pasaran")
def harga_pasaran_padang():
    return {
        "lokasi": "Padang - Update 2026",
        "semen_padang_50kg": 65000,
        "bata_merah_per_buah": 800,
        "batako_per_buah": 3500,
        "hebel_per_m3": 850000,
        "besi_8mm_per_batang": 45000,
        "besi_10mm_per_batang": 65000,
        "pasir_per_m3": 280000,
        "kerikil_per_m3": 300000
    }
