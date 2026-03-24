"""
main.py - AgriSense Uygulama Giriş Noktası
=============================================
FastAPI uygulamasını başlatır, router'ları dahil eder
ve veritabanı tablolarını oluşturur.

Çalıştırma:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.db.session import Base, engine

# Veritabanı tablolarını oluştur (yoksa)
Base.metadata.create_all(bind=engine)

# FastAPI uygulama örneği
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
)

# API router'ını dahil et
app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    """API kök endpoint'i — sağlık kontrolü."""
    return {
        "proje": settings.PROJECT_NAME,
        "versiyon": settings.VERSION,
        "durum": "çalışıyor",
        "dokümantasyon": "/docs",
    }
