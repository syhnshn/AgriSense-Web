"""
schemas.py - Pydantic Doğrulama Şemaları (Task 3)
====================================================
Veri doğrulama ve serileştirme için Pydantic modellerini içerir.
Her tablo için Base, Create ve Response şemaları tanımlanmıştır.

- Base: Ortak alanları tanımlar
- Create: Yeni kayıt oluştururken kullanılır (ID gibi otomatik alanlar hariç)
- Response: API yanıtlarında kullanılır (tüm alanlar dahil)

`from_attributes = True` → Pydantic v2'de ORM nesnelerinden doğrudan veri okuması.
"""

import uuid
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


# ========================
# KULLANICI ŞEMALARI
# ========================
class KullaniciBase(BaseModel):
    """Kullanıcı için ortak alanlar."""
    ad_soyad: str = Field(..., min_length=2, max_length=150, description="Kullanıcının adı ve soyadı")
    email: EmailStr = Field(..., description="Kullanıcının e-posta adresi (benzersiz)")


class KullaniciCreate(KullaniciBase):
    """
    Yeni kullanıcı oluşturmak için kullanılan şema.
    ID ve kayıt tarihi otomatik üretilir.
    """
    pass


class KullaniciResponse(KullaniciBase):
    """API yanıtlarında kullanıcı bilgilerini döndürme şeması."""
    id: uuid.UUID
    kayit_tarihi: datetime

    model_config = {"from_attributes": True}


# ========================
# TARLA ŞEMALARI
# ========================
class TarlaBase(BaseModel):
    """Tarla için ortak alanlar."""
    tarla_adi: str = Field(..., min_length=1, max_length=200, description="Tarlanın adı")
    ekin_turu: str = Field(..., min_length=1, max_length=100, description="Ekilen ürün türü")
    ekim_tarihi: date = Field(..., description="Ekim yapılan tarih")
    enlem: float = Field(..., ge=-90, le=90, description="Tarlanın enlemi")
    boylam: float = Field(..., ge=-180, le=180, description="Tarlanın boylamı")


class TarlaCreate(TarlaBase):
    """Yeni tarla oluşturma şeması. Kullanıcı UUID'si zorunludur."""
    kullanici_id: uuid.UUID = Field(..., description="Tarla sahibi kullanıcının UUID'si")


class TarlaResponse(TarlaBase):
    """API yanıtlarında tarla bilgilerini döndürme şeması."""
    id: int
    kullanici_id: uuid.UUID

    model_config = {"from_attributes": True}


# ========================
# SORU CEVAP GEÇMİŞİ ŞEMALARI
# ========================
class SoruCevapBase(BaseModel):
    """Soru-cevap kaydı için ortak alanlar."""
    ciftci_sorusu: str = Field(..., min_length=1, description="Çiftçinin sorduğu soru")
    ai_cevabi: str = Field(..., min_length=1, description="AI tarafından verilen cevap")


class SoruCevapCreate(SoruCevapBase):
    """Yeni soru-cevap kaydı oluşturma şeması."""
    tarla_id: int = Field(..., description="İlgili tarlanın ID'si")


class SoruCevapResponse(SoruCevapBase):
    """API yanıtlarında soru-cevap geçmişini döndürme şeması."""
    id: int
    tarla_id: int
    islem_tarihi: datetime

    model_config = {"from_attributes": True}


# ========================
# HAVA DURUMU LOG ŞEMALARI
# ========================
class HavaDurumuLogBase(BaseModel):
    """Hava durumu kaydı için ortak alanlar."""
    sicaklik: float = Field(..., description="Ölçülen sıcaklık (°C)")
    nem: float = Field(..., ge=0, le=100, description="Nem oranı (%)")
    risk_durumu: str = Field(..., max_length=100, description="Risk durumu değerlendirmesi")


class HavaDurumuLogCreate(HavaDurumuLogBase):
    """Yeni hava durumu kaydı oluşturma şeması."""
    tarla_id: int = Field(..., description="İlgili tarlanın ID'si")


class HavaDurumuLogResponse(HavaDurumuLogBase):
    """API yanıtlarında hava durumu loglarını döndürme şeması."""
    id: int
    tarla_id: int
    olcum_tarihi: datetime

    model_config = {"from_attributes": True}
