import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from functools import lru_cache

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ada di .env / Vercel Env")
genai.configure(api_key=API_KEY)

# MODEL V3 - PALING PINTAR & MURAH
model = genai.GenerativeModel('gemini-1.5-flash')

# CACHE BIAR GAK BOROS GEMINI
@lru_cache(maxsize=100)
def _call_gemini(prompt: str):
    try:
        res = model.generate_content(prompt)
        return res.text.strip()
    except Exception as e:
        return f"ERROR_GEMINI: {str(e)}"

def generate_deskripsi_pasagadang(nama, kategori, harga, tipe="properti"):
    tipe = tipe.lower()
    harga_str = f"Rp {int(harga):,}".replace(",", ".") if str(harga).isdigit() else str(harga)
    
    if tipe == "properti":
        prompt = f"Tulis deskripsi jualan PROPERTI {nama} ({kategori}) harga {harga_str} untuk Pasa Gadang Padang. Hook: LENGKAP. ESTETIK. BISA ONLINE. 3 paragraf pendek, bahasa Padang gaul 'sanak bro', sebut SHM, listrik, air, akses jalan. CTA: Klik WA, stok terbatas. Max 150 kata."
    elif tipe == "estetika":
        prompt = f"Tulis deskripsi BAHAN ESTETIKA {nama} {kategori} harga {harga_str}. Hook: Rumah Biasa Jadi Villa? Rahasianya Ini. Fokus: bikin rumah indah, instagramable, tetangga iri. Sebut tahan lama, motif mewah, harga grosir. CTA: Pesan online Pasa Gadang. Max 120 kata."
    else:
        prompt = f"Tulis deskripsi MATERIAL {nama} {kategori} harga {harga_str}. Hook: Jangan Beli Sembarangan! Fokus: Hemat jutaan, stok 2000+ ready, bisa pesan online kirim hari ini. Bahasa tukang to the point. CTA: Klik WA kunci harga pabrik. Max 100 kata."
    
    return _call_gemini(prompt)

def generate_seo(nama, kategori, tipe="properti"):
    prompt = f"""
    Buatkan SEO untuk {tipe} {nama} {kategori} Pasa Gadang Padang.
    Output harus JSON valid tanpa markdown:
    {{"title": "judul max 60 karakter", "slug": "slug-url-kebab-case", "meta": "meta description max 155 karakter", "keywords": "keyword1, keyword2, keyword3"}}
    """
    raw = _call_gemini(prompt)
    try:
        # bersihkan ```json
        clean = raw.replace("```json","").replace("```","").strip()
        return json.loads(clean)
    except:
        slug = nama.lower().replace(" ","-")+"-padang"
        return {"title": f"{nama} {kategori} - Pasa Gadang", "slug": slug, "meta": f"Jual {nama} {kategori} harga pabrik di Pasa Gadang Padang. LENGKAP. ESTETIK. BISA ONLINE.", "keywords": f"{nama}, {kategori}, Pasa Gadang"}

def generate_blog_post(topik):
    prompt = f"Tulis artikel blog 600 kata untuk Pasa Gadang tentang '{topik}'. Struktur: Hook LENGKAP ESTETIK BISA ONLINE, 3 subjudul H2, tips praktis, akhiri CTA beli di Pasa Gadang. Bahasa SEO friendly."
    return _call_gemini(prompt)

def generate_hemat(nama, harga_jual, harga_pasaran):
    try:
        hemat = int(harga_pasaran) - int(harga_jual)
        if hemat <=0: return ""
        prompt = f"Buat 1 kalimat jualan nampol: Beli {nama} di Pasa Gadang hemat Rp {hemat:,} dibanding pasaran Rp {harga_pasaran:,}. Bahasa FOMO."
        return _call_gemini(prompt)
    except:
        return f"Hemat jutaan beli {nama} di Pasa Gadang!"

def generate_all_in_one(nama, kategori, harga, tipe="properti", harga_pasaran=0):
    """V3 CORE - 1 KLIK JADI 4"""
    deskripsi = generate_deskripsi_pasagadang(nama, kategori, harga, tipe)
    seo = generate_seo(nama, kategori, tipe)
    hemat = generate_hemat(nama, harga, harga_pasaran) if harga_pasaran else ""
    
    wa_caption = f"{seo['title']} - {hemat} {deskripsi[:100]}... Pesan online: pasagadang.com/{tipe}/{seo['slug']}"
    
    return {
        "deskripsi": deskripsi,
        "seo": seo,
        "hemat_text": hemat,
        "wa_caption": wa_caption,
        "blog_idea": f"Cara Memilih {nama} yang Benar Biar Rumah Estetik"
    }

# COMPATIBILITY BUAT KODE LAMA LU
def generate_deskripsi(merek, tahun, km, harga):
    return generate_deskripsi_pasagadang(f"{merek} {tahun}", f"KM {km}", harga, tipe="properti")
