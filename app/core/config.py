"""
config.py - Merkezi Konfigürasyon Modülü
==========================================
Pydantic BaseSettings kullanarak ortam değişkenlerini yönetir.
.env dosyasından otomatik olarak değerleri okur.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Uygulama ayarları.
    Tüm değerler .env dosyasından veya ortam değişkenlerinden okunur.
    """

    # Proje bilgileri
    PROJECT_NAME: str = "AgriSense"
    PROJECT_DESCRIPTION: str = "AI-powered digital agriculture assistant"
    VERSION: str = "1.0.0"

    # PostgreSQL Veritabanı bağlantı URL'si
    DATABASE_URL: str

    class Config:
        # .env dosyasından değişkenleri oku
        env_file = ".env"
        env_file_encoding = "utf-8"


# Tek bir ayar nesnesi oluştur (Singleton pattern)
settings = Settings()
