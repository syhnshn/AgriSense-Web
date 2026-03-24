"""
crud.py - CRUD İşlemleri Modülü (Task 4)
==========================================
Veritabanı üzerinde temel CRUD işlemlerini gerçekleştiren fonksiyonları içerir.

Fonksiyonlar:
    - kullanici_olustur / kullanici_getir
    - tarla_olustur / tarla_getir / tarlalari_listele
    - hava_durumu_log_olustur
    - soru_cevap_kaydet
"""

import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.models.models import HavaDurumuLog, Kullanici, SoruCevapGecmisi, Tarla
from app.schemas.schemas import (
    HavaDurumuLogCreate,
    KullaniciCreate,
    SoruCevapCreate,
    TarlaCreate,
)


# ========================
# KULLANICI İŞLEMLERİ
# ========================
def kullanici_olustur(db: Session, kullanici: KullaniciCreate) -> Kullanici:
    """
    Yeni bir kullanıcı oluşturur ve veritabanına kaydeder.

    Args:
        db: Aktif veritabanı oturumu
        kullanici: Kullanıcı oluşturma şeması (ad_soyad, email)

    Returns:
        Kullanici: Oluşturulan kullanıcı ORM nesnesi
    """
    yeni_kullanici = Kullanici(
        ad_soyad=kullanici.ad_soyad,
        email=kullanici.email,
    )
    db.add(yeni_kullanici)
    db.commit()
    db.refresh(yeni_kullanici)
    return yeni_kullanici


def kullanici_getir(db: Session, kullanici_id: uuid.UUID) -> Optional[Kullanici]:
    """
    Verilen UUID'ye sahip kullanıcıyı veritabanından getirir.

    Args:
        db: Aktif veritabanı oturumu
        kullanici_id: Aranacak kullanıcının UUID'si

    Returns:
        Kullanici veya None: Bulunan kullanıcı, bulunamazsa None
    """
    return db.query(Kullanici).filter(Kullanici.id == kullanici_id).first()


# ========================
# TARLA İŞLEMLERİ
# ========================
def tarla_olustur(db: Session, tarla: TarlaCreate) -> Tarla:
    """
    Yeni bir tarla kaydı oluşturur.
    Not: İlgili kullanıcının veritabanında mevcut olması gerekir (FK kısıtlaması).

    Args:
        db: Aktif veritabanı oturumu
        tarla: Tarla oluşturma şeması

    Returns:
        Tarla: Oluşturulan tarla ORM nesnesi
    """
    yeni_tarla = Tarla(
        kullanici_id=tarla.kullanici_id,
        tarla_adi=tarla.tarla_adi,
        ekin_turu=tarla.ekin_turu,
        ekim_tarihi=tarla.ekim_tarihi,
        enlem=tarla.enlem,
        boylam=tarla.boylam,
    )
    db.add(yeni_tarla)
    db.commit()
    db.refresh(yeni_tarla)
    return yeni_tarla


def tarla_getir(db: Session, tarla_id: int) -> Optional[Tarla]:
    """
    Verilen ID'ye sahip tarlayı veritabanından getirir.

    Args:
        db: Aktif veritabanı oturumu
        tarla_id: Aranacak tarlanın ID'si

    Returns:
        Tarla veya None: Bulunan tarla, bulunamazsa None
    """
    return db.query(Tarla).filter(Tarla.id == tarla_id).first()


def tarlalari_listele(db: Session, kullanici_id: uuid.UUID) -> list[Tarla]:
    """
    Belirli bir kullanıcıya ait tüm tarlaları listeler.

    Args:
        db: Aktif veritabanı oturumu
        kullanici_id: Tarlaları listelenecek kullanıcının UUID'si

    Returns:
        list[Tarla]: Kullanıcıya ait tarlaların listesi
    """
    return db.query(Tarla).filter(Tarla.kullanici_id == kullanici_id).all()


# ========================
# HAVA DURUMU LOG İŞLEMLERİ
# ========================
def hava_durumu_log_olustur(db: Session, log: HavaDurumuLogCreate) -> HavaDurumuLog:
    """
    Yeni bir hava durumu kaydı oluşturur.

    Args:
        db: Aktif veritabanı oturumu
        log: Hava durumu log oluşturma şeması

    Returns:
        HavaDurumuLog: Oluşturulan hava durumu log ORM nesnesi
    """
    yeni_log = HavaDurumuLog(
        tarla_id=log.tarla_id,
        sicaklik=log.sicaklik,
        nem=log.nem,
        risk_durumu=log.risk_durumu,
    )
    db.add(yeni_log)
    db.commit()
    db.refresh(yeni_log)
    return yeni_log


# ========================
# SORU CEVAP GEÇMİŞİ İŞLEMLERİ
# ========================
def soru_cevap_kaydet(db: Session, soru_cevap: SoruCevapCreate) -> SoruCevapGecmisi:
    """
    Yeni bir soru-cevap geçmişi kaydı oluşturur.

    Args:
        db: Aktif veritabanı oturumu
        soru_cevap: Soru-cevap oluşturma şeması

    Returns:
        SoruCevapGecmisi: Oluşturulan soru-cevap geçmişi ORM nesnesi
    """
    yeni_kayit = SoruCevapGecmisi(
        tarla_id=soru_cevap.tarla_id,
        ciftci_sorusu=soru_cevap.ciftci_sorusu,
        ai_cevabi=soru_cevap.ai_cevabi,
    )
    db.add(yeni_kayit)
    db.commit()
    db.refresh(yeni_kayit)
    return yeni_kayit
