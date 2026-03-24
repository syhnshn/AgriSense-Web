"""
models.py - SQLAlchemy ORM Modelleri (Task 2)
===============================================
Veritabanı tablolarını Python sınıfları olarak tanımlar.

Tablolar:
    - Kullanici: Çiftçi/kullanıcı bilgileri (UUID PK)
    - Tarla: Tarla ve ekin bilgileri
    - SoruCevapGecmisi: AI soru-cevap geçmişi
    - HavaDurumuLog: Hava durumu ölçüm kayıtları

İlişkiler (One-to-Many):
    - Kullanici → Tarla
    - Tarla → SoruCevapGecmisi
    - Tarla → HavaDurumuLog
"""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


# ========================
# KULLANICI TABLOSU
# ========================
class Kullanici(Base):
    """
    Kullanıcı (çiftçi) bilgilerini tutan tablo.
    Her kullanıcı birden fazla tarlaya sahip olabilir.
    """
    __tablename__ = "kullanici"

    # UUID birincil anahtar - PostgreSQL tarafından otomatik üretilir
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    ad_soyad: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    kayit_tarihi: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=text("NOW()")
    )

    # İlişki: Bir kullanıcının birden fazla tarlası olabilir
    tarlalar: Mapped[list["Tarla"]] = relationship(
        "Tarla", back_populates="kullanici", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Kullanici(id={self.id}, ad_soyad='{self.ad_soyad}', email='{self.email}')>"


# ========================
# TARLA TABLOSU
# ========================
class Tarla(Base):
    """
    Tarla bilgilerini tutan tablo.
    Her tarla bir kullanıcıya aittir ve birden fazla soru-cevap / hava durumu kaydına sahip olabilir.
    """
    __tablename__ = "tarla"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kullanici_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("kullanici.id"), nullable=False
    )
    tarla_adi: Mapped[str] = mapped_column(String(200), nullable=False)
    ekin_turu: Mapped[str] = mapped_column(String(100), nullable=False)
    ekim_tarihi: Mapped[date] = mapped_column(Date, nullable=False)
    enlem: Mapped[float] = mapped_column(Float, nullable=False)
    boylam: Mapped[float] = mapped_column(Float, nullable=False)

    # İlişkiler
    kullanici: Mapped["Kullanici"] = relationship("Kullanici", back_populates="tarlalar")
    soru_cevaplar: Mapped[list["SoruCevapGecmisi"]] = relationship(
        "SoruCevapGecmisi", back_populates="tarla", cascade="all, delete-orphan"
    )
    hava_durumlari: Mapped[list["HavaDurumuLog"]] = relationship(
        "HavaDurumuLog", back_populates="tarla", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Tarla(id={self.id}, tarla_adi='{self.tarla_adi}', ekin_turu='{self.ekin_turu}')>"


# ========================
# SORU CEVAP GEÇMİŞİ TABLOSU
# ========================
class SoruCevapGecmisi(Base):
    """
    AI soru-cevap geçmişini tutan tablo.
    Her kayıt bir tarlaya bağlıdır.
    """
    __tablename__ = "soru_cevap_gecmisi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tarla_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tarla.id"), nullable=False
    )
    ciftci_sorusu: Mapped[str] = mapped_column(Text, nullable=False)
    ai_cevabi: Mapped[str] = mapped_column(Text, nullable=False)
    islem_tarihi: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=text("NOW()")
    )

    # İlişki: Bu kayıt hangi tarlaya ait
    tarla: Mapped["Tarla"] = relationship("Tarla", back_populates="soru_cevaplar")

    def __repr__(self) -> str:
        return f"<SoruCevapGecmisi(id={self.id}, tarla_id={self.tarla_id})>"


# ========================
# HAVA DURUMU LOG TABLOSU
# ========================
class HavaDurumuLog(Base):
    """
    Hava durumu ölçüm kayıtlarını tutan tablo.
    Her kayıt bir tarlaya bağlıdır ve sıcaklık, nem, risk durumu bilgilerini içerir.
    """
    __tablename__ = "hava_durumu_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tarla_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tarla.id"), nullable=False
    )
    sicaklik: Mapped[float] = mapped_column(Float, nullable=False)
    nem: Mapped[float] = mapped_column(Float, nullable=False)
    risk_durumu: Mapped[str] = mapped_column(String(100), nullable=False)
    olcum_tarihi: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=text("NOW()")
    )

    # İlişki: Bu kayıt hangi tarlaya ait
    tarla: Mapped["Tarla"] = relationship("Tarla", back_populates="hava_durumlari")

    def __repr__(self) -> str:
        return f"<HavaDurumuLog(id={self.id}, tarla_id={self.tarla_id}, sicaklik={self.sicaklik})>"
