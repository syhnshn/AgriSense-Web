"""
routes.py - REST API Endpoint'leri
====================================
FastAPI Router ile tüm CRUD endpoint'lerini tanımlar.
Her endpoint, ilgili CRUD fonksiyonunu çağırarak veritabanı işlemlerini gerçekleştirir.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.schemas import (
    HavaDurumuLogCreate,
    HavaDurumuLogResponse,
    KullaniciCreate,
    KullaniciResponse,
    SoruCevapCreate,
    SoruCevapResponse,
    TarlaCreate,
    TarlaResponse,
)
from app.services.crud import (
    hava_durumu_log_olustur,
    kullanici_getir,
    kullanici_olustur,
    soru_cevap_kaydet,
    tarla_getir,
    tarla_olustur,
    tarlalari_listele,
)

router = APIRouter()


# ========================
# KULLANICI ENDPOINT'LERİ
# ========================
@router.post("/kullanicilar/", response_model=KullaniciResponse, tags=["Kullanıcılar"])
def yeni_kullanici(kullanici: KullaniciCreate, db: Session = Depends(get_db)):
    """Yeni bir kullanıcı oluşturur."""
    return kullanici_olustur(db=db, kullanici=kullanici)


@router.get("/kullanicilar/{kullanici_id}", response_model=KullaniciResponse, tags=["Kullanıcılar"])
def kullanici_detay(kullanici_id: uuid.UUID, db: Session = Depends(get_db)):
    """Belirli bir kullanıcının bilgilerini getirir."""
    db_kullanici = kullanici_getir(db=db, kullanici_id=kullanici_id)
    if db_kullanici is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return db_kullanici


# ========================
# TARLA ENDPOINT'LERİ
# ========================
@router.post("/tarlalar/", response_model=TarlaResponse, tags=["Tarlalar"])
def yeni_tarla(tarla: TarlaCreate, db: Session = Depends(get_db)):
    """Yeni bir tarla kaydı oluşturur."""
    return tarla_olustur(db=db, tarla=tarla)


@router.get("/tarlalar/{tarla_id}", response_model=TarlaResponse, tags=["Tarlalar"])
def tarla_detay(tarla_id: int, db: Session = Depends(get_db)):
    """Belirli bir tarlanın bilgilerini getirir."""
    db_tarla = tarla_getir(db=db, tarla_id=tarla_id)
    if db_tarla is None:
        raise HTTPException(status_code=404, detail="Tarla bulunamadı")
    return db_tarla


@router.get("/tarlalar/kullanici/{kullanici_id}", response_model=list[TarlaResponse], tags=["Tarlalar"])
def kullanici_tarlalari(kullanici_id: uuid.UUID, db: Session = Depends(get_db)):
    """Belirli bir kullanıcıya ait tüm tarlaları listeler."""
    return tarlalari_listele(db=db, kullanici_id=kullanici_id)


# ========================
# HAVA DURUMU LOG ENDPOINT'LERİ
# ========================
@router.post("/hava-durumu-log/", response_model=HavaDurumuLogResponse, tags=["Hava Durumu"])
def yeni_hava_durumu_log(log: HavaDurumuLogCreate, db: Session = Depends(get_db)):
    """Yeni bir hava durumu kaydı oluşturur."""
    return hava_durumu_log_olustur(db=db, log=log)


# ========================
# SORU CEVAP ENDPOINT'LERİ
# ========================
@router.post("/soru-cevap/", response_model=SoruCevapResponse, tags=["Soru-Cevap"])
def yeni_soru_cevap(soru_cevap: SoruCevapCreate, db: Session = Depends(get_db)):
    """Yeni bir soru-cevap geçmişi kaydı oluşturur."""
    return soru_cevap_kaydet(db=db, soru_cevap=soru_cevap)
