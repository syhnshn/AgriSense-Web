"""
session.py - Veritabanı Bağlantı Modülü (Task 1)
===================================================
SQLAlchemy 2.0 kullanarak PostgreSQL veritabanına bağlantı kurar.
- Engine: Veritabanı bağlantı havuzunu yönetir.
- SessionLocal: Her istek için bağımsız bir oturum (session) sağlar.
- Base: Tüm ORM modellerinin miras alacağı temel sınıf (DeclarativeBase).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# SQLAlchemy engine oluştur
# pool_pre_ping: Bağlantının hâlâ aktif olup olmadığını kontrol eder
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)

# Oturum fabrikası (session factory) oluştur
# autocommit=False: İşlemler manuel olarak commit edilmelidir
# autoflush=False: Veritabanına otomatik flush yapılmaz, kontrol geliştiriciye aittir
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    Tüm ORM modellerinin miras alacağı temel sınıf.
    SQLAlchemy 2.0'ın modern DeclarativeBase yaklaşımı kullanılmaktadır.
    """
    pass


def get_db():
    """
    Veritabanı oturumu sağlayan generator fonksiyon.
    FastAPI'de dependency injection için kullanılır.

    Yields:
        Session: Aktif veritabanı oturumu
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
